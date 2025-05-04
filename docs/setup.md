# Setting up TuSK

Assuming you have completed the instructions in the [installation guide](<https://github.com/TutlaMC/TuSK/blob/main/docs/home.md#installation>) you may now setup your bot. 

## Customizing TuSK

Before you write scripts you might want to setup your panel so you can operate your bot through Discord. So first you'll want to add your user ID as owner to `config.json`. Let's see how to do that and change other settings using `config.json`

When you open `config.json` you will see something like:

```json
{
    "debug": false,
    "roles":{
        "owners":[],
        "admins":[],
        "developers":[]
    },
    "version":"0.0.1"
}
```

If you want to for example add yourself as the owner you will first have to copy your user ID (you'll first have to enable developer mode on your account, if you are too lazy for this just use /userinfo or /user on a bot like Tutla Assistance or Dyno to get your user ID) and then put it `owners` (put your user ID inside the square brackets so it looks something like this: `"owners":[19347908173920]`)    

From here on you can use /panel to operate your bot.

### Discord RPC (Status)

To change your Discord RPC you have to use `/rpc` (or modify `config.json`). It will then give you a menu to choose between adding or removing a status.

## Skripting

To start *skripting* read [creating skripts](https://github.com/TutlaMC/TuSK/blob/main/docs/skripts.md)