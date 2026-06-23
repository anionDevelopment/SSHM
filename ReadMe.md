# SSHM

SSHM is a [OpenSSH for Windows](https://github.com/PowerShell/openssh-portable)-Fork.

Purpose:
SSH has some annoying "features" which should protect the keys of the users.
You have to set some permissions for your key-files.
This makes it tricky on Windows because Windows-permissions are a little bit different in comparison to the unix-permissions.
And this causes annoying errors on Windows (especially when you have a usb-device with your keys which you are using on multiple of your machines) which are useless anyway because on Windows you can access the keys anyway, you just have to set permissions.
To avoid this, this fork has removed these checks.
Removed? Isn't this a security risk?
No. You are responsible for your keys. It is absolutely unusual that you provide keys in your custom folder and your application says "I take care of the security". Much more: Securing keys is only working if you ensure your keys are protected *always* and not only when your SSH-client does a check because it just currently want to use the keys.
Checking whether a key is being stored insecurely when it's used, and then potentially denying the connection, is like checking your front door key to see if someone has made an unauthorized copy.
And this check only happens when you're actually trying to use it to unlock the door.
And if there's a suspicion of an unauthorized copy, it prevents the door from opening.
That makes absolutely no sense.
Using a key and checking for an unauthorized copy (which isn't even properly checked) are two completely unrelated things.
And combining these two things doesn't increase security.
If you want that SSH tries to take care about the security anyway, then SSHM is not the right tool for you. You can just use SSH.
But do you want that? Did you ever thought "For security I rely on the not-working permission-constraint managed by SSH" which prevents that I can use my keys instead of showing me a warning when the permissions may be to broad?
No. You are responsible to protect your keys. Always. Everywhere.
SSH only checks file-level permissions reactively, not proactively. If SSH refuses the connection, this doesn't change the fact that an attacker might already have the keys due to the too broad permissions.
And if you want to take care of your keys by yourself, then you do not need a SSH-connection-denial-of-service because SSH thinks your keys are stored unsafe.
(If this is would be the case, you would have to revoke and replace your keys anyway as soon as possible.)
So, and if you take care of your keys the sometimes-protection-checks inside of the application become useless, but they are still annoying.
That is why they are removed in this fork.

## Apply updates from upstream

```
git fetch upstream --no-tags
git subtree pull --prefix=Other/Resources/Upstream upstream latestw_all
```
