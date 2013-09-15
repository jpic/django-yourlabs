{% if False %}

Start a new project with this template:

    django-admin.py startproject -e rst,py,md,Makefile --template=https://github.com/yourlabs/yourlabs-project-template/zipball/master your_project_name

    cd your_project_name/docs
    make html

    # If you don't want to read the docs yet then go ahead with:
    ./manage.py syncdb
    ./manage.py migrate
    ./manage.py runserver

{% endif %}

# {{ project_name|title }}


