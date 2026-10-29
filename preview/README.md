# BigPicture Sweden website

This repository contains the source code for the BigPicture Sweden website. The
website is built with [Quarto](https://quarto.org).


## View the website locally

1. Clone this repository to your local machine.

2. [Install the Quarto CLI](https://quarto.org/docs/get-started/).

3. To preview the website, `cd` to the repo's top-level folder and type the
   following on the command line:

    ```bash
    quarto preview
    ```


## Publish changes to GitHub Pages

1. Create a new branch and commit your changes to it.

2. You may want to render the project locally to make sure the website looks ok:

    ```bash
    quarto render
    ```

    The rendered output will be stored in the `/docs` folder.

3. Create a pull request to merge your changes into the main branch.


## Configuring the website

General settings are stored in the file `_quarto.yml`, global variables in
the file `_variables.yml`, and variables that might need to be changed using
environment variables in `_environment`.

Settings that are specific to the deployed version are set in [github
environment](https://github.com/imi-bigpicture/portal.bigpicture.eu/settings/environments).
The local configuration of these variables should be set in the file
`_environment.local`, which will not be tracked by git:

```
CAPTHAKEY=recaptchasitekey
SKULD=url_to_skuld
```

## License

[The MIT License](https://opensource.org/licenses/MIT)
