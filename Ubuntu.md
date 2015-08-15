### Ubuntu Linux ###

We are recommend to use [Ubuntu Linux](http://www.ubuntu.com/) instead of Microsoft Windows Operation System.


### Eclipse IDE ###

  1. in terminal type command, and wait while installed eclipse _(~250 Mb)_
```
sudo aptitude install eclipse-pde
```
  1. run eclipse and go to **`Help -> Install new software -> Add`** and add new update sites
```
Name: Eclipse
Update site: http://download.eclipse.org/eclipse/updates/3.5.x

Name: PyDev
Update site: http://pydev.org/updates

Name: GAE
Location: http://dl.google.com/eclipse/plugin/3.5

Name: Mercurial
Update site: http://cbes.javaforge.com/update

Name: GIT
Update site: http://download.eclipse.org/egit/updates

Name: SVN
Update site: http://download.eclipse.org/technology/subversive/0.7/update-site/
```
  1. install plugins and restart Eclipse after complete installation of each plugin:
    1. PyDev for Eclipse
    1. source control support: Mercurial, GIT _(Eclipse Egit)_, SVN _(Team provider, Team provider UI)_
    1. Google plugin for Plugin


### Commands shortcuts ###

Your **Google App Engine SDK** should be placed in `/home/[username]/workspace/appengine/`.

You can [checkout GAE SDK](http://code.google.com/p/googleappengine/source/checkout) instead of download code in archive.

```
# edit file with commands
sudo nano ~/.bashrc

# after this lines
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# insert this code
alias install='sudo apt-get update && sudo apt-get install'
alias update='sudo apt-get update && sudo apt-get upgrade'
alias gae='clear; ~/workspace/appengine/dev_appserver.py'
alias gaedeploy='clear; ~/workspace/appengine/appcfg.py update
```

Finally, restart your Ubuntu PC for make changes.

```
gae ~/workspace/mysite.com/src/

# or this
cd ~/workspace
gae mysite.com/src/

# deploy to server
gaedeploy ~/workspace/mysite.com/src/
```