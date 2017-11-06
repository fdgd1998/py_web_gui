#!/usr/bin/env python2.7
import os, sys, shutil, json
from subprocess import call
from distutils.dir_util import copy_tree

def replace_with_file(src_file, token, replacement_file):
  with open(src_file, "r+") as sf, open(replacement_file, "r") as rf:
    src = sf.read()
    rep = rf.read()
    sf.seek(0)
    sf.truncate()
    sf.write(src.replace(token, rep))

def replace_with_str(src_file, token, replacement_str):
  with open(src_file, "r+") as sf:
    src = sf.read()
    sf.seek(0)
    sf.truncate()
    sf.write(src.replace(token, replacement_str))

def create_staging_assignment(settings):
  # create staging area
  staging_dir = "." + settings.assignment_type + ("_%s" % str(settings.assignment_num))
  if os.path.exists(staging_dir):
    shutil.rmtree(staging_dir)
  os.makedirs(staging_dir)

  # From assignment
  copy_tree( "%s/" % settings.assignment_path, "%s/" % staging_dir)

  # From infra
  copy_tree( "%s" % settings.infra_path, "%s/" % staging_dir)

  if settings.has_ui:
    # fix ui html
    replace_with_str("%s/ui/index.html" % staging_dir, "[[ title ]]", settings.assignment_name)

    script_string = ""
    if settings.script_imports:
        script_string = "\n".join([ "<script src=\"%s\"></script>" % s for s in settings.script_imports])
    replace_with_str("%s/ui/index.html" % staging_dir, "[[ script_imports ]]", script_string)

    style_string = ""
    if settings.style_imports:
        style_string = "\n".join([ "<link rel=\"stylesheet\" href=\"%s\">" %s for s in settings.style_imports])
    replace_with_str("%s/ui/index.html" % staging_dir, "[[ style_imports ]]", style_string)

    replace_with_file("%s/ui/index.html" % staging_dir, "[[ ui ]]", "%s/ui/index.html" % settings.assignment_path)

    # fix ui script
    replace_with_file("%s/ui/ui.js" % staging_dir, "[[ ui ]]", "%s/ui/ui.js" % settings.assignment_path)

  # copy empty assignment
  shutil.copy("%s/empty.py" % settings.assignment_path, staging_dir + "/" + settings.assignment_type + ".py")

  # prepare zip file, render markdown
  zip_filename = "%s.zip" % staging_dir[1:]
  if os.path.exists(zip_filename):
    os.remove(zip_filename)

  root = os.getcwd()
  os.chdir(staging_dir)

  for md in settings.markdown:
    call(["./build_md.sh", md])

  if settings.has_ui:
    call(["zip", "-r", zip_filename, "ui"])
    call(["zip", "-jr", zip_filename, "server.py", "RPCServerHandler.py"])
  call(["zip", "-r", zip_filename, "cases", "resources"])
  call(["zip", "-jr", zip_filename, "test.py",
                                    "verifier.py",
                                    "wrapper.py",
                                    settings.assignment_type+".py"] + ["%s.pdf" % x for x in settings.markdown])
  os.chdir(root)
  shutil.copy(staging_dir+"/"+zip_filename, zip_filename)

  # clean up
  shutil.rmtree(staging_dir)

  # create a solution
  solution_path = "solution%s" % staging_dir
  if os.path.exists(solution_path):
    shutil.rmtree(solution_path)
  os.makedirs(solution_path)

  # unzip assignment
  call(["unzip", zip_filename, "-d", solution_path])

  # copy solution
  shutil.copy("%s/solution.py" % settings.assignment_path, solution_path + "/" + settings.assignment_type + ".py")

def create_staging_analyzer(settings):
  # create staging area
  staging_dir = ".analyzer_" + settings.assignment_type + ("_%s" % str(settings.assignment_num))
  if os.path.exists(staging_dir):
    shutil.rmtree(staging_dir)
  os.makedirs(staging_dir)

  # from assignment:
  # wrapper.py, verifier.py cases resources
  shutil.copy( settings.assignment_path + "/wrapper.py", "%s/wrapper.py" % staging_dir)
  shutil.copy( settings.assignment_path + "/verifier.py", "%s/verifier.py" % staging_dir)
  copy_tree( settings.assignment_path + "/cases/", "%s/cases" % staging_dir)
  copy_tree( settings.assignment_path + "/resources/", "%s/resources" % staging_dir)

  # analyzer core files
  shutil.copy( settings.infra_path + "/analyzer/Dockerfile", "%s/Dockerfile" % staging_dir)
  shutil.copy( settings.infra_path + "/analyzer/mapper.py", "%s/mapper.py" % staging_dir)
  shutil.copy( settings.infra_path + "/analyzer/reducer.py", "%s/reducer.py" % staging_dir)
  shutil.copy( settings.infra_path + "/analyzer/mapreduced.yml", "%s/mapreduced.yml" % staging_dir)

  # rewrite test count in mapreduced.yml
  test_count = len([x for x in os.listdir('%s/cases/' % staging_dir) if x.endswith(".in")])
  replace_with_str("%s/mapreduced.yml" % staging_dir, "[[ test_count ]]", str(test_count))
  # rewrite module name in mapper.py
  replace_with_str("%s/mapper.py" % staging_dir, "[[ module_name ]]", settings.assignment_type)

  # create zip file
  zip_filename = "%s.zip" % staging_dir
  if os.path.exists(zip_filename):
    os.remove(zip_filename)

  root = os.getcwd()
  os.chdir(staging_dir)
  zip_filename = "%s.zip" % staging_dir[1:]

  call(["zip", "-r", zip_filename, "cases", "resources"])
  call(["zip", "-jr", zip_filename, "Dockerfile",
                                    "mapper.py",
                                    "reducer.py",
                                    "mapreduced.yml",
                                    "wrapper.py",
                                    "verifier.py"])
  os.chdir(root)
  shutil.copy(staging_dir+"/"+zip_filename, zip_filename)

  # clean up
  shutil.rmtree(staging_dir)

class Settings:
    def __init__(self, assignment_path):
      self.assignment_path = assignment_path

      with open("%s/config.json" % assignment_path, 'r') as f:
        c = json.loads(f.read())
        self.assignment_type = c["assignment_type"]
        self.assignment_name = c["assignment_name"]
        self.has_ui = False if ("has_ui" not in c) else c["has_ui"]
        self.assignment_num = c["assignment_num"]
        self.infra_path = "infra"
        self.markdown = c["markdown"]
        self.script_imports = [] if ("script_imports" not in c) else c["script_imports"]
        self.style_imports = [] if ("style_imports" not in c) else c["style_imports"]

def print_usage():
  print "PROPER USAGE OF THE BUILD ASSIGNMENT TOOL:"
  print "%s <path to assignment folder>" % sys.argv[0]
  print "\nto render markdown, need \"gem install github-markup\", and wkhtmltopdf from http://wkhtmltopdf.org/downloads.html"

def main():
  if len(sys.argv) < 2:
    print_usage()
    sys.exit(1)

  settings = Settings(sys.argv[1])
  create_staging_assignment(settings)
  create_staging_analyzer(settings)

if __name__ == '__main__':
  main()

