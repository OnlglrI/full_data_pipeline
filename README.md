# Ошибка при запуске DAG в Airflow (dbt + Cosmos)

При запуске DAG `update_dbt_models.py` возникла ошибка:

Broken DAG: [/opt/airflow/dags/update_dbt_models.py]
Traceback (most recent call last):
File "/home/airflow/.local/lib/python3.10/site-packages/cosmos/dbt/graph.py", line 271, in load_via_dbt_ls
stdout = run_command(deps_command, tmpdir_path, env)
File "/home/airflow/.local/lib/python3.10/site-packages/cosmos/dbt/graph.py", line 94, in run_command
raise CosmosLoadDbtException(f"Unable to run {command} due to the error:\n{details}")
cosmos.dbt.graph.CosmosLoadDbtException: Unable to run ['/home/airflow/.local/bin/dbt', 'deps', '--project-dir', '/opt/airflow/tmp/tmp_5235y1w', '--profiles-dir', '/opt/airflow/tmp/tmpiljme5os', '--profile', 'default', '--target', 'dev'] due to the error:
[0m10:34:00 Running with dbt=1.7.14
[0m10:34:02 Encountered an error:
[Errno 13] Permission denied: '/opt/airflow/tmp/tmp_5235y1w/package-lock.yml'
[0m10:34:02 Traceback (most recent call last):
File "/home/airflow/.local/lib/python3.10/site-packages/dbt/cli/requires.py", line 91, in wrapper
result, success = func(*args, **kwargs)
File "/home/airflow/.local/lib/python3.10/site-packages/dbt/cli/requires.py", line 76, in wrapper
return func(*args, **kwargs)
File "/home/airflow/.local/lib/python3.10/site-packages/dbt/cli/requires.py", line 152, in wrapper
return func(*args, **kwargs)
File "/home/airflow/.local/lib/python3.10/site-packages/dbt/cli/requires.py", line 198, in wrapper
return func(*args, **kwargs)
File "/home/airflow/.local/lib/python3.10/site-packages/dbt/cli/main.py", line 492, in deps
results = task.run()
File "/home/airflow/.local/lib/python3.10/site-packages/dbt/task/deps.py", line 221, in run
self.lock()
File "/home/airflow/.local/lib/python3.10/site-packages/dbt/task/deps.py", line 200, in lock
with open(lock_filepath, "w") as lock_obj:


## Возможная причина

Ошибка указывает на **проблемы с правами доступа** при записи файла `package-lock.yml` в директорию `/opt/airflow/tmp/`.

## Что проверить

1. У кого права на каталог `/tmp` и вложенные временные папки:
   ```bash
   ls -ld /tmp
   ls -l/tmp

drwxrwxrwt   1 root    root  4096 Aug 28 11:00 tmp

## Что я думаю не так
проблема в том что он почему то создает свою директориб под ROOT пользователем 
Astranomer пишет под свою директорию под ROOT и потом сам не может туда записать
P.s если я правильно понял ошибку 