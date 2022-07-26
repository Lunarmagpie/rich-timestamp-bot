# Rich Timestamp Bot
A discord bot to help you create rich timestamps for discord.

https://user-images.githubusercontent.com/65521138/180729461-b83ea916-88f6-44d4-9e0e-71d04be35367.mov

[Invite Link](https://discord.com/oauth2/authorize?client_id=1000892742165090384&scope=bot&permissions=0)

# Formatting
| Format          | Example                        |
|-----------------|--------------------------------|
| Short Time      | 3:00 PM                        |
| Long Time       | 3:00:00 PM                     |
| Short Date      | 07/26/2022                     |
| Long Date       | July 26, 2022                  |
| Short Date/Time | July 26, 2022 3:00 PM          |
| Long Date/Time  | Tuesday, July 26, 2022 3:00 PM |
| Relative Time   | in 12 hours                    |

## Self Hosting
```sh
poetry shell
poetry install
maturin develop  # only need to do this once
poetry run bot
```
