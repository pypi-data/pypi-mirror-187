# kopeechka

**kopeechka** - This module is a representation of the kopeechka.store API in Python

**API documentation RUS** [ https://link.kopeechka.store/CzXxp6?lang=ru&k=API]( https://link.kopeechka.store/CzXxp6?lang=ru&k=API)

**API documentation ENG** [https://link.kopeechka.store/CzXxp6?lang=en&k=API](https://link.kopeechka.store/CzXxp6?lang=en&k=API)

# Installation

Install the current version with PyPI:

```python
pip install kopeechka
```

## Usage

You can get a token in your personal account on the kopeechka.store website

```python
from kopeechka import MailActivations

body = MailActivations(token="TOKEN")
```

## Exception handling

You can import all exceptions from kopeechka.errors

List of all exceptions with description:

	ACTIVATION_CANCELED - The mail was canceled.
	ACTIVATION_NOT_FOUND - First letter has not been received, reorder isn't possible.
	BAD_BALANCE - There are not enough funds to perform the operation.
	BAD_COMMENT - Activattion not found (It's not your activation).
	BAD_DOMAIN - We do not have such a domain/domain zone.
	BAD_EMAIL - Mail was banned.
	BAD_SITE - You specified the site incorrectly.
	BAD_TOKEN - Invalid token.
	NO_ACTIVATION - Invalid TASK_ID activation.
	OUT_OF_STOCK - There is no mail with such settings. Try changing MAIL_TYPE or write to support - we'll try to add mailboxes.
	SYSTEM_ERROR - Unknown, system error. Contact support - we will help!
	TIME_LIMIT_EXCEED - The limit of mail orders per second has been reached (applies to special tariffs), it is necessary to expand the tariff.
	WAIT_LINK - The letter hasn't arrived yet.
    UNKNOWN_ERROR - Unknown error (the text of the exception may be different in different situations.)

## Types

You can import all types from kopeechka.types_kopeechka

## Sync methods

You can import all methods from kopeechka.methods

## Sync example

```python
from kopeechka import MailActivations
from kopeechka.errors import BAD_TOKEN

body = MailActivations(token="TOKEN")

#balance request
try:
    data = body.user_balance()
    print(data.data) # returns a dictionary with data from json
    print(data.balance) # returns a user balance
    print(data.status) # returns a response status
except BAD_TOKEN as e:
    print(e) # returns a string with an error
    print(e.data) # returns the data received by api Kopeechka

#mail request
try:
    data = body.mailbox_get_email(site="site", mail_type="mail_type", sender="sender", regex="regex", soft_id=0, investor=0, subject="subject")
    print(data.data) # returns a dictionary with data from json
    print(data.status) # returns a response status
    print(data.id) # returns a task_id this mail
    print(data.mail) #returns a email address
except BAD_TOKEN as e:
    print(e)  # returns a string with an error
    print(e.data)  # returns the data received by api Kopeechka

#letter request
try:
    data = body.mailbox_get_message(full=0, id=123)
    print(data.data)  # returns a dictionary with data from json
    print(data.status)  # returns a response status
    print(data.value) # returns a url
    print(data.fullmessage) # returns a full message from email
except BAD_TOKEN as e:
    print(e)  # returns a string with an error
    print(e.data)  # returns the data received by api Kopeechka

#cancel mail
try:
    data = body.mailbox_cancel(id=123)
    print(data.data)  # returns a dictionary with data from json
    print(data.status)  # returns a response status
except BAD_TOKEN as e:
    print(e)  # returns a string with an error
    print(e.data)  # returns the data received by api Kopeechka

#reorder mail
try:
    data = body.mailbox_reorder(site="site", email="email", regex="regex", subject="subject")
    print(data.data)  # returns a dictionary with data from json
    print(data.status)  # returns a response status
    print(data.id)  # returns a task_id this mail
    print(data.mail)  # returns a email address
except BAD_TOKEN as e:
    print(e)  # returns a string with an error
    print(e.data)  # returns the data received by api Kopeechka

#find ID activation of email
try:
    data = body.mailbox_get_fresh_id(site="site", email="email")
    print(data.data)  # returns a dictionary with data from json
    print(data.status)  # returns a response status
    print(data.id)  # returns a task_id this mail
except BAD_TOKEN as e:
    print(e)  # returns a string with an error
    print(e.data)  # returns the data received by api Kopeechka

#set a comment to the ordered mail
try:
    data = body.mailbox_set_comment(id=123, comment="comment")
    print(data.data)  # returns a dictionary with data from json
    print(data.status)  # returns a response status
except BAD_TOKEN as e:
    print(e)  # returns a string with an error
    print(e.data)  # returns the data received by api Kopeechka

#mail search by parameters
try:
    data = body.mailbox_get_bulk(count=1, comment="comment", email="email", site="site")
    print(data.data)  # returns a dictionary with data from json
    print(data.status)  # returns a response status
    print(data.count) # returns a count of items
    print(data.items) # returns a list with found data
    for item in data.items:
        print(item.data) # returns a dictionary with data from json
        print(item.id) # returns a task_id
        print(item.service) # returns a service
        print(item.email) # returns a email
        print(item.date) # returns a date
        print(item.status) # returns a status
        print(item.value) # returns a link
        print(item.comment) # returns a comment
except BAD_TOKEN as e:
    print(e)  # returns a string with an error
    print(e.data)  # returns the data received by api Kopeechka

#list of all service domains
try:
    data = body.mailbox_get_domains(site="site")
    print(data.data)  # returns a dictionary with data from json
    print(data.status)  # returns a response status
    print(data.count) # returns a count of items
    print(data.domains) # returns a list with domains
except BAD_TOKEN as e:
    print(e)  # returns a string with an error
    print(e.data)  # returns the data received by api Kopeechka

#get prices and zones
data = body.mailbox_zones(popular=1, zones=1)
print(data.data)  # returns a dictionary with data from json
print(data.status)  # returns a response status
print(data.popular) # returns a list with populars
for item in data.popular:
    print(item.data) # returns a dictionary with data from json
    print(item.name) # returns a name
    print(item.count) # returns a count
    print(item.cost) # returns a cost
print(data.zones) # returns a list with zones
for item in data.zones:
    print(item.data) # returns a dictionary with data from json
    print(item.name) # returns a name
    print(item.cost) # returns a cost
```

## Async methods

You can import all async methods from kopeechka.async_methods

## Async example

```python
from kopeechka import AsyncMailActivations
from kopeechka.errors import BAD_TOKEN
import asyncio

async def main():

    body = AsyncMailActivations('TOKEN')

    # balance request
    try:
        data = await body.user_balance()
        print(data.data)  # returns a dictionary with data from json
        print(data.balance)  # returns a user balance
        print(data.status)  # returns a response status
    except BAD_TOKEN as e:
        print(e)  # returns a string with an error
        print(e.data)  # returns the data received by api Kopeechka

    # mail request
    try:
        data = await body.mailbox_get_email(site="site", mail_type="mail_type", sender="sender", regex="regex", soft_id=0,
                                      investor=0, subject="subject")
        print(data.data)  # returns a dictionary with data from json
        print(data.status)  # returns a response status
        print(data.id)  # returns a task_id this mail
        print(data.mail)  # returns a email address
    except BAD_TOKEN as e:
        print(e)  # returns a string with an error
        print(e.data)  # returns the data received by api Kopeechka

    # letter request
    try:
        data = await body.mailbox_get_message(full=0, id=123)
        print(data.data)  # returns a dictionary with data from json
        print(data.status)  # returns a response status
        print(data.value)  # returns a url
        print(data.fullmessage)  # returns a full message from email
    except BAD_TOKEN as e:
        print(e)  # returns a string with an error
        print(e.data)  # returns the data received by api Kopeechka

    # cancel mail
    try:
        data = await body.mailbox_cancel(id=123)
        print(data.data)  # returns a dictionary with data from json
        print(data.status)  # returns a response status
    except BAD_TOKEN as e:
        print(e)  # returns a string with an error
        print(e.data)  # returns the data received by api Kopeechka

    # reorder mail
    try:
        data = await body.mailbox_reorder(site="site", email="email", regex="regex", subject="subject")
        print(data.data)  # returns a dictionary with data from json
        print(data.status)  # returns a response status
        print(data.id)  # returns a task_id this mail
        print(data.mail)  # returns a email address
    except BAD_TOKEN as e:
        print(e)  # returns a string with an error
        print(e.data)  # returns the data received by api Kopeechka

    # find ID activation of email
    try:
        data = await body.mailbox_get_fresh_id(site="site", email="email")
        print(data.data)  # returns a dictionary with data from json
        print(data.status)  # returns a response status
        print(data.id)  # returns a task_id this mail
    except BAD_TOKEN as e:
        print(e)  # returns a string with an error
        print(e.data)  # returns the data received by api Kopeechka

    # set a comment to the ordered mail
    try:
        data = await body.mailbox_set_comment(id=123, comment="comment")
        print(data.data)  # returns a dictionary with data from json
        print(data.status)  # returns a response status
    except BAD_TOKEN as e:
        print(e)  # returns a string with an error
        print(e.data)  # returns the data received by api Kopeechka

    # mail search by parameters
    try:
        data = await body.mailbox_get_bulk(count=1, comment="comment", email="email", site="site")
        print(data.data)  # returns a dictionary with data from json
        print(data.status)  # returns a response status
        print(data.count)  # returns a count of items
        print(data.items)  # returns a list with found data
        for item in data.items:
            print(item.data)  # returns a dictionary with data from json
            print(item.id)  # returns a task_id
            print(item.service)  # returns a service
            print(item.email)  # returns a email
            print(item.date)  # returns a date
            print(item.status)  # returns a status
            print(item.value)  # returns a link
            print(item.comment)  # returns a comment
    except BAD_TOKEN as e:
        print(e)  # returns a string with an error
        print(e.data)  # returns the data received by api Kopeechka

    # list of all service domains
    try:
        data = await body.mailbox_get_domains(site="site")
        print(data.data)  # returns a dictionary with data from json
        print(data.status)  # returns a response status
        print(data.count)  # returns a count of items
        print(data.domains)  # returns a list with domains
    except BAD_TOKEN as e:
        print(e)  # returns a string with an error
        print(e.data)  # returns the data received by api Kopeechka

    # get prices and zones
    data = await body.mailbox_zones(popular=1, zones=1)
    print(data.data)  # returns a dictionary with data from json
    print(data.status)  # returns a response status
    print(data.popular)  # returns a list with populars
    for item in data.popular:
        print(item.data)  # returns a dictionary with data from json
        print(item.name)  # returns a name
        print(item.count)  # returns a count
        print(item.cost)  # returns a cost
    print(data.zones)  # returns a list with zones
    for item in data.zones:
        print(item.data)  # returns a dictionary with data from json
        print(item.name)  # returns a name
        print(item.cost)  # returns a cost

loop = asyncio.new_event_loop()
loop.run_until_complete(main())
```