=====================================================================
 Aipo: Simple AsyncIO task/job queue execution framework
=====================================================================

:Version: 0.1.0
:Download: http://pypi.org/project/aipo
:Source: http://github.com/CaiqueReinhold/aipo
:Keywords: asyncio, task, job, queue

What is Aipo?
=============

Aipo is a minimal framework for dispatching and running background tasks using asynchronous python.

Using the task decorator you can turn your python functions into tasks that can be dispatched to a queue and executed in the aipo server.

Setting up your aipo app::

    app = Aipo(config='aipo.yaml')

    @app.task
    async def my_task():
        await get_stuff()
        await comunicate_stuff()


Once you execute you task it will be dispatched to the queue and executed in the aipo server::

    await my_task()

Run your Aipo server using the command line::
    aipo run --config aipo.yaml


Installation
=============

You can install Aipo from the Python Package Index (PyPI).

To install using `pip`::

    $ pip install aipo


Currently supported Aipo backends
==================================

- Redis


Currently supported event loops
================================

- asyncio
- uvloop
