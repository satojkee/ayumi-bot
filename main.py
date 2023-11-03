import asyncio

from ayumi.api import session


if __name__ == '__main__':
    # Using async bot -> asyncio required for polling
    # Using none_stop=True -> to ignore errors
    asyncio.run(session.polling(none_stop=True))
