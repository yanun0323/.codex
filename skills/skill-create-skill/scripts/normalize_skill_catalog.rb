#!/usr/bin/env ruby
# frozen_string_literal: true

require 'fileutils'
require 'optparse'
require 'yaml'

options = {
  skills_root: 'skills',
  icons_dir: File.expand_path('../references/icons', __dir__),
  check: false
}

OptionParser.new do |opts|
  opts.banner = 'Usage: normalize_skill_catalog.rb [options]'

  opts.on('--skills-root PATH', 'Skills root path (default: skills)') do |value|
    options[:skills_root] = value
  end

  opts.on('--icons-dir PATH', 'Shared icons directory') do |value|
    options[:icons_dir] = value
  end

  opts.on('--check', 'Validate only; do not modify files') do
    options[:check] = true
  end
end.parse!

def skill_dirs(skills_root)
  Dir.glob(File.join(skills_root, '**', 'SKILL.md'), File::FNM_DOTMATCH)
     .sort
     .map { |path| File.dirname(path) }
end

def classify_basename(base)
  if base.start_with?('agents-')
    target = "rule-#{base.delete_prefix('agents-')}"
    return { target_base: target, label: 'Rule', icon: 'rule-small.svg', stem: target.delete_prefix('rule-') }
  end

  if base.start_with?('rule-')
    return { target_base: base, label: 'Rule', icon: 'rule-small.svg', stem: base.delete_prefix('rule-') }
  end

  if base.start_with?('command-')
    return { target_base: base, label: 'Command', icon: 'command-small.svg', stem: base.delete_prefix('command-') }
  end

  if base.start_with?('skill-')
    return { target_base: base, label: 'Skill', icon: 'skill-small.svg', stem: base.delete_prefix('skill-') }
  end

  target = "skill-#{base}"
  { target_base: target, label: 'Skill', icon: 'skill-small.svg', stem: target.delete_prefix('skill-') }
end

def titleize(stem)
  stem.split('-').reject(&:empty?).map { |token| token[0].upcase + token[1..].downcase }.join(' ')
end

def replace_frontmatter_name(skill_md_path, expected_name, check)
  content = File.read(skill_md_path)
  lines = content.lines

  first = lines.index("---\n")
  return ['SKILL.md missing frontmatter start', false] if first.nil?

  second = nil
  ((first + 1)...lines.length).each do |idx|
    if lines[idx] == "---\n"
      second = idx
      break
    end
  end
  return ['SKILL.md missing frontmatter end', false] if second.nil?

  changed = false
  name_found = false

  ((first + 1)...second).each do |idx|
    next unless lines[idx].start_with?('name:')

    name_found = true
    desired = "name: #{expected_name}\n"
    if lines[idx] != desired
      lines[idx] = desired
      changed = true
    end
  end

  unless name_found
    lines.insert(first + 1, "name: #{expected_name}\n")
    changed = true
  end

  if changed && !check
    File.write(skill_md_path, lines.join)
  end

  [nil, changed]
end

def load_yaml(path)
  return {} unless File.exist?(path)
  return {} if File.zero?(path)

  parsed = YAML.safe_load(File.read(path), aliases: true)
  parsed.is_a?(Hash) ? parsed : {}
rescue StandardError
  {}
end

def update_openai_yaml(path, display_name, icon_small, check)
  data = load_yaml(path)
  interface = data['interface']
  interface = {} unless interface.is_a?(Hash)

  changed = false
  if interface['display_name'] != display_name
    interface['display_name'] = display_name
    changed = true
  end

  if interface['icon_small'] != icon_small
    interface['icon_small'] = icon_small
    changed = true
  end

  data['interface'] = interface

  if changed && !check
    out = YAML.dump(data, line_width: -1).sub(/^---\n/, '')
    FileUtils.mkdir_p(File.dirname(path))
    File.write(path, out)
  end

  changed
end

errors = []
changes = []

root = options[:skills_root]
icons_dir = options[:icons_dir]

required_icons = {
  'rule-small.svg' => File.join(icons_dir, 'rule-small.svg'),
  'command-small.svg' => File.join(icons_dir, 'command-small.svg'),
  'skill-small.svg' => File.join(icons_dir, 'skill-small.svg')
}

required_icons.each do |name, path|
  errors << "Missing source icon: #{path}" unless File.exist?(path)
end

if errors.any?
  warn errors.join("\n")
  exit 1
end

# Step 1: rename directories if needed
skill_dirs(root).each do |dir|
  base = File.basename(dir)
  info = classify_basename(base)
  target = info[:target_base]
  next if base == target

  new_dir = File.join(File.dirname(dir), target)
  if File.exist?(new_dir)
    errors << "Cannot rename #{dir} -> #{new_dir}: target exists"
    next
  end

  changes << "rename #{dir} -> #{new_dir}"
  FileUtils.mv(dir, new_dir) unless options[:check]
end

# Step 2: normalize files after rename
skill_dirs(root).each do |dir|
  base = File.basename(dir)
  info = classify_basename(base)

  expected_name = info[:target_base]
  label = info[:label]
  icon_file = info[:icon]
  display_name = "#{label} - #{titleize(info[:stem])}"
  icon_small = "./assets/#{icon_file}"

  skill_md = File.join(dir, 'SKILL.md')
  err, changed = replace_frontmatter_name(skill_md, expected_name, options[:check])
  if err
    errors << "#{skill_md}: #{err}"
  elsif changed
    changes << "update name #{skill_md} => #{expected_name}"
  end

  assets_dir = File.join(dir, 'assets')
  icon_src = required_icons[icon_file]
  icon_dst = File.join(assets_dir, icon_file)
  unless File.exist?(icon_dst)
    changes << "copy icon #{icon_dst}"
    unless options[:check]
      FileUtils.mkdir_p(assets_dir)
      FileUtils.cp(icon_src, icon_dst)
    end
  end

  openai_path = File.join(dir, 'agents', 'openai.yaml')
  if update_openai_yaml(openai_path, display_name, icon_small, options[:check])
    changes << "update openai #{openai_path}"
  elsif !File.exist?(openai_path)
    changes << "create openai #{openai_path}"
  end

  if options[:check]
    # verify values in check mode as well
    yaml = load_yaml(openai_path)
    interface = yaml['interface'].is_a?(Hash) ? yaml['interface'] : {}
    if interface['display_name'] != display_name
      errors << "display_name mismatch in #{openai_path}: expected '#{display_name}'"
    end
    if interface['icon_small'] != icon_small
      errors << "icon_small mismatch in #{openai_path}: expected '#{icon_small}'"
    end

    unless File.exist?(icon_dst)
      errors << "missing icon asset #{icon_dst}"
    end
  end
end

if options[:check]
  if errors.any?
    warn errors.join("\n")
    exit 1
  end

  puts 'OK: skill catalog is normalized.'
  exit 0
end

if errors.any?
  warn errors.join("\n")
  exit 1
end

puts 'Applied changes:'
puts(changes.empty? ? '- none' : changes.map { |line| "- #{line}" }.join("\n"))
