[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)

# nptr-cli

> Manage your uploads to 0x0.st from the cli.

`nptr-cli` exists to easily upload to 0x0.st via the cli.
It also prints the tokens to delete uploads from 0x0.st.

It also can be used as a library for other python projects.

## Installation

```shell
pip install nptr-cli
```

## Usage

To upload files:
```shell
$ 0x0 u file.txt # you can also use `0x0 up` or `0x0 upload`
$ echo "this will be uploaded" | 0x0 # You can omit the u, it is the default when you pipe into `0x0`
$ 0x0 -i https://your-0x0-instance.com u file.txt # To use other instances than 0x0.st
$ 0x0 -i alias u file.txt # can also be an alias defined in your config.toml
$ 0x0 u -s file.txt # To use longer paths in the URL which are harder to predict like https://0x0.st/s/123acb-319gas8dgh8ahdg8/a8gn.txt
```
All these commands will output something like this:
```
https://0x0.st/abcd.txt
Expires: 1234567890
Token: TOKEN
```

To delete files:
```shell
$ 0x0 d TOKEN URL # you can also use `0x0 del` or `0x0 delete`
```

To get more info about 0x0 use:

```shell
$ 0x0 -h
$ 0x0 delete -h
$ 0x0 upload -h
```

## Configuration

The config file is located at `~/.config/0x0/config.toml`.

These are the default values currently, if nothing is set (See also [#Usage]).
```toml
quiet=false # same as -q/--quiet
instance=https://0x0.st # same as -i/--instance
secret=false # same as -s/--secret
```

As mentioned earlier you can also add instance aliases and basic auth credentials.

### Instance Aliases
Aliases work like this:
````toml
[instances]

[instances.my_instance] # now you can use `0x0 -i my_instance`
url = https://my_instance.tld # it will use this domain
username = admin # and if you provide a username
password = admin # and password (which are optional),
# it will authenticate via http basic auth
````

Also have a look at the [documentation](https://jonas-w.github.io/nptr-cli)
