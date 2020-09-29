# Example project

In this example project we are going to build a simple project management software.
Logged in users will be able to create projects. When a `Project` is created by a `User`, this user becomes a project's owner.
A project owner can add other users to a project and specify their role in a project (member or reporter).
Project members can create and resolve issues, reporters can only create issues.

Since we are build

## Access permissions

Superuser - can do everything

Project owner - can create new projects, manage project members, CRUD all projects and issues

- can create new project
- view own projects
- can manage own project including:
  - changing project details (name, description)
  - managing (CRUD) project members
  - managing (CRUD) project issues, including assigning members to issues

Project member can:

- view projects he belongs to,
- create issues in a projects he belongs to,
- edit own issues, including assigning issues to other project members,
- change status of issues he is assigned to,

Project reporter:

- can view projects he is assigned to,
- can create issues in a projects he is assigned to,
