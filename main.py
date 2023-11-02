import asyncio

from ayumi.api import session


if __name__ == '__main__':
    # Polling
    asyncio.run(session.polling(none_stop=True))
