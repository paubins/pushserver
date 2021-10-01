createdb pushserver;
grant all privileges on database pushserver to pushserver;
create user pushserver with encrypted password 'rdbUYT8nFrnMyWwbxRvduikM';

python3 manage.py startapp pushtokens

