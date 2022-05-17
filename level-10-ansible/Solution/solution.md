# Ansible challenge

The goal of this challenge is to find the commit containing the passphrase used to vault the SSH password for the robot configuration servers. Once obtained, the password can be used to decrypt the vaulted SSH password stored in the hosts file.

## Solution 1 

Users can clone the repo and use either the GOGS gui or the git CLI tool to look at prior commits. 

In the GUI you can click the commits link and view th ecommit History. Commit 5ac51b0028 will show the contents of the .vault_pass file

In the CLI you can run the following command:

```bash
git log -p
```

This will also eventually show the contents of .vault_pass

```bash
commit 34073c9e7bc07f8f6105858ac3408e61d1185fa6
Author: G00dspeed <cory.goodspeed@intel.com>
Date:   Tue Mar 29 15:18:52 2022 -0700

    Removing vault file

diff --git a/.vault_pass b/.vault_pass
deleted file mode 100644
index 24d0e76..0000000
--- a/.vault_pass
+++ /dev/null
@@ -1 +0,0 @@
-{d0nT-c0mM17-$3cR37$}
\ No newline at end of file
```

## Solution 2

With the vault password in hand you can now decrypt the vaulted SSH password for the remote hosts: [ansible documentation](https://docs.ansible.com/ansible/latest/user_guide/vault.html#viewing-encrypted-variables) will provide instructions on how to do this.

The following command will reveal the password which serves as the second flag:

```bash
cgoodspe@ubuntu:~/Documents/ansible-playbooks$ ansible localhost -m ansible.builtin.debug -a var="all['vars']['ansible_password']" -e "@hosts" --vault-id .vault_pass 
localhost | SUCCESS => {
    "all['vars']['ansible_password']": "{f@1L-@7-$c@l3}",
    "changed": false
}
```