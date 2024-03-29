# tailogsTelegramBot
tailogsTelegramBot – - код <a href="https://t.me/TailogsTelegramBot">моего телеграм бота</a>

Пользуюсь услугами <a href="https://hostvds.com/">этого хостинга</a> и полностью доволен. Кручу на `ubuntu`.

---

Чтобы установить эту программу, вам необходимо скопировать этот репозиторий в выбранную вами директорию с помощью команды:

```git
git clone https://github.com/tailogs/tailogsTelegramBot.git
```

---

После этого создайте venv внутри установленного каталога и активируйте ее соответствующими командами:

```python
python -m venv venv
```

Для Windows:

```python
venv\Scripts\activate.bat
```

Для Linux и MacOS:

```python
source venv/bin/activate
```

---

Откройте консоль, перейдите в каталог программы и введите следующую команду для установки всех модулей:

```python
pip install -r requirements.txt
```


Создайте базу данных `users.db` который содержит таблицу `users` и следующие поля:

```sql
user_id - Числовое поле, not null, уникальный
username - Текстовое поле, not null, уникальный
```

Создать ещё одну таблицу `user_chats` со следующими полями:

```sql
chat_id - Числовое поле, not null, уникальный
users - Текстовое поле, not null, уникальный
```

---

Теперь вы можете запустить программу командой:

```python
python main.py
```

Или, если вы используете Windows, дважды щелкните файл active.bat.
