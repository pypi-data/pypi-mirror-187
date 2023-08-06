# Data examples

This page provides examples of the various data that the Launchable CLI sends to the Launchable service.

You can use the `--dry-run` global option to preview what data _would_ be passed in a real request. You can also use the `--log-level audit` global option when you invoke the CLI to view exactly what data was passed in the request. See the [CLI reference](../../resources/cli-reference.md) for more info about both of these options.

## Recording builds

e.g. `launchable record build --name 549854157 --source .`

### Request 1: Create a build

`POST` body sent to the Launchable API:

```javascript
{
  "buildNumber": "549854157",
  "commitHashes": [
    {
      "repositoryName": ".",
      "commitHash": "8fc4e65781dc63605d336b1883497f051daff946"
    }
  ]
}
```

### Request 2: Record commits

{% hint style="info" %}
The CLI scrubs PII from commit details prior to data transmission. Full names are removed, and email addresses are hashed **** using the **** SHA-256 algorithm.

Note that email addresses are _hashed_, not _encrypted:_ encryption implies that Launchable can decrypt the stored value back to the original email address; hashing means Launchable cannot. Therefore **the CLI does not collect email addresses**.
{% endhint %}

`POST` body sent to the Launchable API:

```javascript
{
  "commits": [
    {
      "id": 0,
      "workspaceId": 0,
      "commitHash": "ff84e8fbcb4ddc88879adc3c49760e2562aba1d8",
      "authorName": "",
      "authorEmailAddress": "994a70d1ac542e847f24abfcbe05e68926c281c81cd13c704964800d58d022e3",
      "authorWhen": 1611341818000,
      "authorTimezoneOffset": -480,
      "committerName": "",
      "committerEmailAddress": "994a70d1ac542e847f24abfcbe05e68926c281c81cd13c704964800d58d022e3",
      "committerWhen": 1611341818000,
      "committerTimezoneOffset": -480,
      "organizationId": 0,
      "parentHashes": {}
    },
    {
      "id": 0,
      "workspaceId": 0,
      "commitHash": "76cf64103a2dfc5c4e62b6c19526dc66e554b34c",
      "authorName": "",
      "authorEmailAddress": "994a70d1ac542e847f24abfcbe05e68926c281c81cd13c704964800d58d022e3",
      "authorWhen": 1611775208000,
      "authorTimezoneOffset": -480,
      "committerName": "",
      "committerEmailAddress": "994a70d1ac542e847f24abfcbe05e68926c281c81cd13c704964800d58d022e3",
      "committerWhen": 1611775208000,
      "committerTimezoneOffset": -480,
      "organizationId": 0,
      "parentHashes": {
        "ff84e8fbcb4ddc88879adc3c49760e2562aba1d8": [
          {
            "id": 0,
            "commitRelationId": 0,
            "linesAdded": 1,
            "linesDeleted": 1,
            "status": "MODIFY",
            "path": "gradle/.gitignore",
            "pathTo": "gradle/.gitignore",
            "organizationId": 0
          },
          {
            "id": 0,
            "commitRelationId": 0,
            "linesAdded": 2,
            "linesDeleted": 2,
            "status": "ADD",
            "path": "/dev/null",
            "pathTo": "gradle/ci.sh",
            "organizationId": 0
          }
        ]
      }
    },
    {
      "id": 0,
      "workspaceId": 0,
      "commitHash": "86a656d2ca948ec5f845e177ae9be7a8ca9a8208",
      "authorName": "",
      "authorEmailAddress": "994a70d1ac542e847f24abfcbe05e68926c281c81cd13c704964800d58d022e3",
      "authorWhen": 1611775770000,
      "authorTimezoneOffset": -480,
      "committerName": "",
      "committerEmailAddress": "994a70d1ac542e847f24abfcbe05e68926c281c81cd13c704964800d58d022e3",
      "committerWhen": 1611775927000,
      "committerTimezoneOffset": -480,
      "organizationId": 0,
      "parentHashes": {
        "76cf64103a2dfc5c4e62b6c19526dc66e554b34c": [
          {
            "id": 0,
            "commitRelationId": 0,
            "linesAdded": 19,
            "linesDeleted": 19,
            "status": "MODIFY",
            "path": "gradle/ci.sh",
            "pathTo": "gradle/ci.sh",
            "organizationId": 0
          }
        ]
      }
    },
    ...
  ]
}
```

## Subsetting tests

e.g. `launchable subset --target 25% --build 549854157 gradle src/test/java`

`POST` body sent to the Launchable API:

```javascript
{
  "testPaths": [
    [
      {
        "type": "class",
        "name": "example.MulTest"
      }
    ],
    [
      {
        "type": "class",
        "name": "example.AddTest"
      }
    ],
    [
      {
        "type": "class",
        "name": "example.SubTest"
      }
    ],
    [
      {
        "type": "class",
        "name": "example.DivTest"
      }
    ]
  ],
  "target": 0.25,
  "session": {
    "id": "6370"
  }
}
```

## Recording test results

e.g. `launchable record test --debug --build 549854157 gradle build/test-results/test/*.xml`

`POST` body sent to the Launchable API:

```javascript
{
  "events": [
    {
      "type": "case",
      "testPath": [
        {
          "type": "class",
          "name": "example.AddTest"
        },
        {
          "type": "testcase",
          "name": "calc"
        }
      ],
      "duration": 0.004,
      "status": 1,
      "stdout": "",
      "stderr": "",
      "created_at": "2021-02-19T21:33:02",
      "data": null
    },
    {
      "type": "case",
      "testPath": [
        {
          "type": "class",
          "name": "example.DivTest"
        },
        {
          "type": "testcase",
          "name": "calc"
        }
      ],
      "duration": 0,
      "status": 1,
      "stdout": "",
      "stderr": "",
      "created_at": "2021-02-19T21:33:02",
      "data": null
    },
    {
      "type": "case",
      "testPath": [
        {
          "type": "class",
          "name": "example.MulTest"
        },
        {
          "type": "testcase",
          "name": "calc"
        }
      ],
      "duration": 0,
      "status": 1,
      "stdout": "",
      "stderr": "",
      "created_at": "2021-02-19T21:33:02",
      "data": null
    },
    {
      "type": "case",
      "testPath": [
        {
          "type": "class",
          "name": "example.SubTest"
        },
        {
          "type": "testcase",
          "name": "calc"
        }
      ],
      "duration": 0.001,
      "status": 1,
      "stdout": "",
      "stderr": "",
      "created_at": "2021-02-19T21:33:02",
      "data": null
    }
  ]
}
```
