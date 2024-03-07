# How to Redeploy the Mobile Robotics Backend

> **Warning:** DO NOT STOP EC2 INSTANCE (old)
>
> This will cause the address that the backend can be accessed at to change. This will therefore need to be changed on the frontend and thus on each teams robot code.

> **Note:** Tmux
>
> Tmux is a Linux command line program that is a multiplexer for Unix systems. This means that it can allow multiple terminal sessions at once. Tmux is especially helpful as it allows users to detach from a session and allow for programs to continue running. Tmux's detach feature allows us to leave the backend server running while leaving the AWS EC2 console.

## How to login to the AWS EC2 server console

1. Login to the AWS account and navigate to the EC2 Dashboard.
2. Make sure that you are looking at the correct location `Europe(Ireland)`. This can be changed with the dropdown in the top right.
3. Press on `Instances (Running)` in the Resources section.
4. Press on EE303Backend's `Instance ID` (this should be in blue).
5. Press on `Connect` on the top right.
6. Insure the username is set to `ubuntu` and press `Connect`.
7. You are now in the EC2 console.

## How to check if the backend server is running (old)

1. Now that the command line is open, you can see what is running by entering `tmux list-sessions`.

   - If the server is currently running something similar to this should be returned `django: 1 windows (created Wed Jan  3 23:05:53 2024)`.
   - If the server is not currently running something similar to this should be returned `no server running on /tmp/tmux-1000/default`.

## If the server is not running (old)

1. Make sure you are in the `MobileRobotics` directory by running `cd MobileRobotics`.
2. Run `tmux new-session -d -s django 'python3 manage.py runserver 0.0.0.0:8000'` this will start the server.
3. Rerun `tmux list-sessions` to confirm that it is currently running.
4. Now you are safe to leave this AWS page.

## If the server is running (old)

1. Run `tmux attach` followed by `CTRL + C` this will stop the server.
2. Make sure you are in the `MobileRobotics` directory by running `cd MobileRobotics`.
3. To restart the server run `tmux new-session -d -s django 'python3 manage.py runserver 0.0.0.0:8000'` this will start the server.
4. Rerun `tmux list-sessions` to confirm that it is currently running.
5. Now you are safe to leave this AWS page.

## How to restart server

1. Run `sudo supervisorctl restart all`

## How to setup AWS EC2 instance

1. Open the Amazon EC2 console at https://console.aws.amazon.com/ec2/
1. Choose Launch Instance.
1. In Step 1: Choose an Amazon Machine Image (AMI) choose `Ubuntu`
1. In Step 2: Choose an Instance Type - `t2.micro`
1. In key pair (login) select `Proceed without a key pair`
1. Press `Launch Instance`

1. Press `View All Instances`
1. Wait until status check passes (`2/2 checks passed`)
1. Go to security tab
1. Press on link under security groups
1. Press `edit inboud rules`
1. Press `add rule`
1. Add `8000` for port range and `0.0.0.0/0` where the magnifiying glass is
1. Press `Save Rules`

## Setup Server on EC2 instance

1. Login to console
1. Clone repo
1. Run `sudo apt-get update && sudo apt install python3-pip -y && sudo apt install python3.10-venv && python3 -m venv myenv && source myenv/bin/activate && pip install -r MobileRobotics/requirements.txt`

1. Run `sudo nano /home/ubuntu/MobileRobotics/monitor.sh`
1. Change the ip address for the ip address of server and save
1. Run `chmod +x /home/ubuntu/MobileRobotics/monitor.sh`
1. Run `sudo apt-get install supervisor`
1. Run `sudo service supervisor restart`
1. Run `sudo nano /etc/supervisor/conf.d/ee303.conf`
1. Copy in

   ```
   [program:manageserver]
   directory=/home/ubuntu/MobileRobotics
   command=/home/ubuntu/myenv/bin/python3 /home/ubuntu/MobileRobotics/manage.py runserver 0.0.0.0:8000
   autostart=true
   autorestart=true
   stderr_logfile=/var/log/manageserver.err.log
   stdout_logfile=/var/log/manageserver.out.log
   minsecs=10

   [program:check_django_endpoint]
   command=/home/ubuntu/MobileRobotics/monitor.sh
   autostart=true
   autorestart=true
   stderr_logfile=/var/log/check_django_endpoint.err.log
   stdout_logfile=/var/log/check_django_endpoint.out.log

   [group:guni]
   programs:manageserver, check_django_endpoint
   ```

1. Run `sudo supervisorctl reread && sudo supervisorctl update && sudo supervisorctl status`
1. Create database by running `python3 /home/ubuntu/MobileRobotics/manage.py migrate`
1. Create admin user by running `python3 /home/ubuntu/MobileRobotics/manage.py createsuperuser` enter a name just press enter to skip email and enter password. (This will be admin user details for adding and removing teams)
1. It should show both programs running
1. Now you can use the ip address in the frontend
