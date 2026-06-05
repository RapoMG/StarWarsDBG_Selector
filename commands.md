# Commands

## Buildozer Docker image
    get image
    ```docker pull kivy/buildozer:latest```

    # PowerShell build run
    ```
    docker run --rm -it `
        -v "${PWD}:/home/user/hostcwd" `
        -v "${env:USERPROFILE}\.buildozer:/home/user/.buildozer" `
        kivy/buildozer android debug
    ```

    # Linux \WSL build run
    ```
    docker run --interactive --tty --rm \
        --volume "$PWD:/home/user/hostcwd" \
        --volume "$HOME\.buildozer":/home/user/.buildozer \
        kivy/buildozer android debug
    ```
    