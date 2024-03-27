#!/usr/bin/env node

const fs = require("fs"),
  path = require("path"),
  template = path.join(path.dirname(__filename), "template"),
  project = process.argv[2] || "project";

try {
  fs.cpSync(template, project, {
    recursive: true,
    force: false,
    errorOnExist: true,
  });
  const pkgFile = path.join(project, "package.json");
  pkg = JSON.parse(fs.readFileSync(pkgFile));
  pkg.name = project;
  fs.writeFileSync(pkgFile, JSON.stringify(pkg, null, 4) + "\n");
  fs.rmSync(path.join(project, "package-lock.json"));
  console.log(`@wq/create: Created ${project} from wq-vite-template`);
} catch (e) {
  console.log(e.message || "@wq/create: Error creating project");
}
