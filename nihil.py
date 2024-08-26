import paramiko
import pyfiglet

def show_banner():
    banner = pyfiglet.figlet_format("Nihil", font="block")
    print(banner)

print("\nCreated by yExqt")

def connect_ssh(hostname, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    return ssh

def configure_firewall(ssh, rules):
    for rule in rules:
        stdin, stdout, stderr = ssh.exec_command(f"sudo iptables {rule}")
        output = stdout.read().decode()
        error = stderr.read().decode()
        if error:
            print(f"Errore nell'eseguire la regola {rule}: {error}")
        else:
            print(f"Regola eseguita correttamente: {rule}\n{output}")

def save_firewall_rules(ssh):
    stdin, stdout, stderr = ssh.exec_command("sudo iptables-save | sudo tee /etc/iptables/rules.v4")
    output = stdout.read().decode()
    error = stderr.read().decode()
    if error:
        print(f"Errore nel salvare le regole del firewall: {error}")
    else:
        print(f"Regole del firewall salvate correttamente.\n{output}")

def main():
    show_banner()  

    hostname = input("metasploitable2 IP: ")
    username = input("username: ")
    password = input("password: ")

    ssh = connect_ssh(hostname, username, password)
                                                                       #in futuro migliorerò questo codice
    rules = []
    while True:
        rule = input("enter 'done' to finish: ")
        if rule.lower() == 'done':
            break
        rules.append(rule)

    configure_firewall(ssh, rules)
    save_firewall_rules(ssh)
    ssh.close()

if __name__ == "__main__":
    main()