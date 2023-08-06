# Choosing a value for \<BUILD NAME>

{% hint style="info" %}
This page relates to [recording-builds-from-multiple-repositories.md](recording-builds-from-multiple-repositories.md "mention").
{% endhint %}

Your CI process probably already relies on some identifier to distinguish different builds. Such an identifier might be called a build number, build ID, etc. Most CI systems automatically make these values available via built-in environment variables. This makes it easy to pass this value into `record build`:

| CI system              | Suggested \<BUILD NAME> value | Documentation                                                                                                                           |
| ---------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| Azure DevOps Pipelines | `Build.BuildId`               | [Link](https://docs.microsoft.com/en-us/azure/devops/pipelines/build/variables)                                                         |
| Bitbucket Pipelines    | `BITBUCKET_BUILD_NUMBER`      | [Link](https://support.atlassian.com/bitbucket-cloud/docs/variables-and-secrets/)                                                       |
| CircleCI               | `CIRCLE_BUILD_NUM`            | [Link](https://circleci.com/docs/2.0/env-vars/#built-in-environment-variables)                                                          |
| GitHub Actions         | `GITHUB_RUN_ID`               | [Link](https://docs.github.com/en/actions/configuring-and-managing-workflows/using-environment-variables#default-environment-variables) |
| GitLab CI              | `CI_JOB_ID`                   | [Link](https://docs.gitlab.com/ee/ci/variables/predefined\_variables.html)                                                              |
| GoCD                   | `GO_PIPELINE_LABEL`           | [Link](https://docs.gocd.org/current/faq/dev\_use\_current\_revision\_in\_build.html#standard-gocd-environment-variables)               |
| Jenkins                | `BUILD_TAG`                   | [Link](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#using-environment-variables)                                               |
| Travis CI              | `TRAVIS_BUILD_NUMBER`         | [Link](https://docs.travis-ci.com/user/environment-variables/#default-environment-variables)                                            |

Other examples:

* If your build produces an artifact or file that is later retrieved for testing, then the `sha1sum` of the file itself would be a good build name as it is unique.
* If you are building a Docker image, its content hash can be used as the unique identifier of a build: `docker inspect -f "{{.Id}}"`.

{% hint style="warning" %}
If you only have one source code repository, it might tempting to use a Git commit hash (or the output of `git-describe`) as the build name, but we discourage this.

It's not uncommon for teams to produce multiple builds from the same commit that are still considered different builds.
{% endhint %}
