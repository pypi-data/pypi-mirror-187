# clean-git-branches

clean-git-branches is a command line utility for cleaning stale branches from your local git repository. The program will check for branches that have been deleted on the remote and prompt the user to confirm before deleting them locally.

## Installation

To install clean, simply run the following command:

```pip3 install clean-git-branches```


## Usage

To use clean-git-branches, navigate to the root of your local git repository in the command line and run the following command:

```clean_git_branches```

It is also possible pass the path as the first argument:
```clean_git_branches "/Users/butler/my_repo/"```

The cleaner is set the be cautious by default, asking the user to verify deleting the local branches.
In order to bypass this, pass ```False``` as the second argument. Examples:
```clean_git_branches "/Users/butler/my_repo/" False```
```clean_git_branches "" False``` - will default the path to the current working directory

The program will then check for stale branches and prompt the user to confirm before deleting them (unless bypassed).

By default, the program will also protect certain branches from being deleted (master, main, dev) in case they exist on the remote repository. To change the list of protected branches, you can modify the "protected_branches" variable in the clean-git-branches.py file.

```Please note that this program is only compatible with Git.```


## Contributing

If you would like to contribute to the development of clean-git-branches, please feel free to fork the repository and submit pull requests with your changes.

## License

clean-git-branches is released under the [MIT License](https://opensource.org/licenses/MIT).

