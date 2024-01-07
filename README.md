# How to Redeploy the Mobile Robotics Backend

> **Warning:** DO NOT STOP EC2 INSTANCE
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

## How to check if the backend server is running

1. Now that the command line is open, you can see what is running by entering `tmux list-sessions`.

   - If the server is currently running something similar to this should be returned `django: 1 windows (created Wed Jan  3 23:05:53 2024)`.
   - If the server is not currently running something similar to this should be returned `no server running on /tmp/tmux-1000/default`.

## If the server is not running

1. Make sure you are in the `MobileRobotics` directory by running `cd MobileRobotics`.
2. Run `tmux new-session -d -s django 'python3 manage.py runserver 0.0.0.0:8000'` this will start the server.
3. Rerun `tmux list-sessions` to confirm that it is currently running.
4. Now you are safe to leave this AWS page.

## If the server is running

1. Run `tmux attach` followed by `CTRL + C` this will stop the server.
2. Make sure you are in the `MobileRobotics` directory by running `cd MobileRobotics`.
3. To restart the server run `tmux new-session -d -s django 'python3 manage.py runserver 0.0.0.0:8000'` this will start the server.
4. Rerun `tmux list-sessions` to confirm that it is currently running.
5. Now you are safe to leave this AWS page.
