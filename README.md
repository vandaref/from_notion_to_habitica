# Description

This project that will sync your Notion tasks to your Habitica account like creation tasks depending of their priority, their status (todo or complete) and close them in order to score in Habitica.

## Installation

Download or clone the repo :

```bash
gh repo clone vandaref/from_notion_to_habitica
```

### Habitica
0. Follow the instructions -> [API_Habitica](https://habitica.fandom.com/wiki/API_Options#API_Token)
1. Get your Habitica API Token (XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXXX)
2. Get your User ID (XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXXX)

### Notion
1. Create an integration -> [Notion Integrations](https://www.notion.so/my-integrations)
2. Get your integration token (secret_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX)
3. Get your databaseId -> [Get your databaseId](https://developers.notion.com/reference/retrieve-a-database)
* How get your databaseId :
  * Try to share your database and copy the link
  * https://www.notion.so/yourusername/**XXXXXXXXXXXXXXXXXXX**?v=...
4. Finally, in Notion, select the database that you want to sync with Habitica. Look for Connections (in settings) and choose the integration that you created.
 
## Setup
Update the values in the script depending on your own API etc.

## Usage

Start the script. 
I suggest to make a cron in order to execute the script few times in a day. (cf. [How to create a cron](https://help.dreamhost.com/hc/en-us/articles/215767047-Creating-a-custom-Cron-Job))
```
python3 from_notion_to_habitica.py
```

## Thanks to
[Gauchy](https://gist.github.com/gauchy)
