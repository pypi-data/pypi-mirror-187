# Terminal Kanban Board

## Structure

Users:
- [ ] has a role (Admin, etc.)
- [x] can create project
- [ ] can delete project
- [x] can create task
- [ ] can delete task
- [ ] can check all the tasks assigned to them
	- [ ] Maybe only Admin can do so?
- [x] can assign task to a project
- [x] can set due date
- [ ] can change status
	- [ ] of a task
	- [ ] of a project
- [ ] can change headline
- [ ] can change description

**UC 1. Users can create tasks**

Task:
- [ ] created by User
- [x] has unique id
- [x] has associated created datetime
- [x ] consists of headline and description
	- [x] If headline is emtpy ("") raise ValueError
	- [x] Description is empty (None) by default
	- [ ] Headline can be changed later on
	- [ ] Description can be changed later on
- [x] can be part of the project
- [x] has assignee
- [x] has due day
- [ ] may contain comments
- [x] has status (Backlog, TODO, In progress, Review, Done)


Commentary:
- [ ] has a datetime associated with them
- [ ] exists only within a task

**UC 2. Users (Admins) can create projects**

Project:
- [ ] has unique id
- [ ] has name
- [ ] has optional description
- [ ] has a status (Active, Archived)
- [ ] can contain tasks
- [ ] can have due date
- [ ] can have collaborators
-

## CLI

- [ ]  tasks
	- [ ]  list
		- [x]  all
		- [x]  based on condition
			- [x]  related to project
			- [ ]  created N days ago and still in backlog / without a project
			- [x]  with a certain status (BACKLOG, TODO, etc.)
			- [x]  assigned to a particular user
			- [ ]  multiple condition of one type (-s "BACKLOG,TODO")
			- [ ]  Not condition (-s "!TODO")
			- [x]  mix of any conditions
	- [x]  create
	- [x]  change (done via `update` method)
		- [x]  name
		- [x]  description
		- [ ]  cannot change immutable attributed (i.e. created_by)
	- [x]  assign (done via `update` method)
	- [x]  change status  (`update` method)
		- [x]   done (`done` method)
	- [x]  associate to project (`update` method)
	- [x]  set due date (`update` method)
			- [ ]  add validation (bring back)
	- [ ]  delete (archive)
	- [ ]  add comment
- [ ]  projects
	- [x]  list
	- [x]  create
	- [ ]  change
		- [ ]  title
		- [ ]  description
	- [ ]  change status (archive)
- [ ]  users
	- [ ]  login
	- [ ]  create
	- [ ]  show assigned tasks
	
## TODO

- [ ] printing in rich is class dependent and should not be hardcoded
