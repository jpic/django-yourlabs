Installing this project
=======================

This chapter covers the basic installation of this project.

Setting up a basic virtual environment (For all users)
------------------------------------------------------

- Install `Vagrant <http://vagrantup.com>`_,
- Clone the project repository with git (`Windows
  <http://windows.github.com/>`_, `MacOSX <http://mac.github.com/>`_),
- Run the `Vagrantfile`.

Setting up a basic local environment (For hardcore users)
---------------------------------------------------------

It is necessary to create a virtual environment per project if you
don't want to pollute your OS with project-specific dependencies.

Also, different projects may depend on different versions (ie.
django 1.4 vs django 1.5) and thus it is a best practice to have a
virtual environment per project checkout.

This is how setting up a local environment looks like::

    # install requirements dependencies, ubuntu example
    sudo apt-get install libmemcached-dev python-dev npm node
    sudo npm install -g recess coffee-script

    # prepare the parent directory for the project
    mkdir {{ project_name }}
    cd {{ project_name }}
    
    # create the virtualenv
    virtualenv {{ project_name }}_env

    # optionnal but appreciated
    ln -sfn {{ project_name }}_env env

    # activate the virtualenv
    source env/bin/activate

    # clone the project
    git clone $REPO_URL {{ project_name }}

    # install requirements
    pip install -r {{ project_name }}/requirements.txt

    # Create database tables
    {{ project_name }}/manage.py syncdb

    # Apply migrations
    {{ project_name }}/manage.py migrate

Your project is now ready to use, you can start a shell with 
`{{ project_name }}/manage.py shell` or a local http server with 
`{{ project_name }}/manage.py runserver`.

What next ?
-----------

From here you can move on to any of these chapters:

- design: if you want to start hacking the frontend,
- dev: if you want to start hacking the python code,
- prod: if you want to deploy the project on a public http server.

..
   Local Variables:
   mode: rst
   fill-column: 79
   End:
   vim: et syn=rst tw=79
