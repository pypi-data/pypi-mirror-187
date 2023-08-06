
# RUNFALCON PIPELINE INTEGRATION TOOLS

This package helps to integrate CI/CD processes with [runfalcon platform](https://www.runfalcon.com)

**REQUIEREMENTS**

None.
  
**USAGE**

```
python3 -m runfalconpipelineintegration <operation> [ags] [<flags>]
```

## Operation `authenticate`
Generates an [authentication token](https://app.runfalcon.com).  This token will be input for secure operations.

### **Examples**

- Generate authentication token

    ```sh
    python3 -m runfalconpipelineintegration authenticate login "myemail@mydomain.com" password "secretpassword"
    ```
    You must replace `myemail@mydomain.com` and `secretpassword` for your valid credentials in runfalcon platform.
    The Output of this operation is an alphanumeric token like this:
    ```
    eyJhbGciOiJIUzI1NiIsInR5cCI6Ikicm9sZXMiOm51bGx9LCJpYXQiOjE2NzIyNTQyMDAsImV4cCI6MTY3MjI2MTQwMH0cWBm8Iua2sUFkHbr89epcfN9EtwBDKtqoLMUtdXJSk
    ```

## Operation `run`
This operation runs a performance testing scenario and waitwait for it to finish.

### **Examples**

- Run a scenario without waiting for it to finish

    ```sh
    python3 -m runfalconpipelineintegration run token "nR5cCI6Ikicm9sZXMiOm51bGYXQiOjE2NzIyNDAsImV4cCI6MTY3MjI2MTQwMH0" client "My client Name" application "My application Name" scenario "My scenario code"
    ```
    You must replace `nR5cCI6Ikicm9sZXMiOm51bGx9LCJpYXQiOjE2NzIyNTQyMDAsImV4cCI6MTY3MjI2MTQwMH0` for a valid authentication token, `My client Name` for your client name in runfalcon platform, `My application Name` for the name of the application in runfalcon platform aich the scneario belongs to, and `My scenario code` for the code of the existing scenario that you want to run.  Add the switch `-q` if you want the command only shows the final response.  The output of the command is a json object that specifies the new job id:
    ```
    {
        "jobId": 1158298, 
        "status": "SUCCESS", 
        "dateCreated": "2023-01-01T17:01:01.851Z", 
        "duration": 178.913196, 
        "kpiLatency": 3000, 
        "kpiErrors": 5, 
        "kpiThroughput": 100, 
        "kpiDeviation": 3000, 
        "metricLatency": 27.74, 
        "metricErrors": 0.35, 
        "metricThroughput": 1659057.06, 
        "metricDeviation": 52.36, 
        "complianceLatency": 199.08, 
        "complianceErrors": 192.94, 
        "complianceThroughput": 200, 
        "complianceDeviation": 198.25
    }
    ```

    Ih this response:

    | Attribute | Type | Description |
    | -- | -- | -- |
    | `jobId` | Job Info | Id corresponding the new created job for this scenario run. |
    | `status` | Job Info | Indicates if the job finished in `SUCCESS` or `ERROR` status. |
    | `dateCreated` | Job Info | Date and time the job starts its execution. |
    | `duration` | Job Info | Indicates the seconds the job took to finalize. |
    | `kpiLatency` | KPI | Objective value defined for the scenario average latency. |
    | `kpiErrors` | KPI | Objective value defined for the scenario errors percentage. |
    | `kpiThroughput` | KPI | Objective value defined for the scenario capacity (requests attended per minute). |
    | `kpiDeviation` | KPI | Objective value defined for the standard deviation for scenario average latency. |
    | `metricLatency` | Metric | Measured value for the scenario average latency in this run (For this `jobId`). |
    | `metricErrors` | Metric | Measured value for the scenario errors percentage in this run (For this `jobId`). |
    | `metricThroughput` | Metric | Measured value for the capacity (requests attended per minute) in this run (For this `jobId`). |
    | `metricDeviation` | Metric | Measured value for the standard deviation for scenario average latency in this run (For this `jobId`). |
    | `complianceLatency` | Compliance | Latency compliance (latency metric vs latency KPI). |
    | `complianceErrors` | Compliance | Errors percentage compliance (Errors percentage metric vs Errors percentage KPI). |
    | `complianceThroughput` | Compliance | Capacity compliance (Capacity metric vs Capacity KPI). |
    | `complianceDeviation` | Compliance | Deviation compliance (Deviation metric vs Deviation KPI). |

