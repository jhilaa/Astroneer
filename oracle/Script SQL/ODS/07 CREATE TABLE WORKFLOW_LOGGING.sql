CREATE TABLE ODS.WORFLOW_LOGGING
(
  loggingDate DATE
, loggingPhase VARCHAR2(2000)
, workflowName VARCHAR2(255)
, workflowFilename VARCHAR2(255)
, workflowStart DATE
, workflowEnd DATE
, workflowLogChannelId VARCHAR2(36)
, workflowParentLogChannelId VARCHAR2(36)
, workflowLogging CLOB
, workflowErrorCount INTEGER
, workflowStatusDescription VARCHAR2(32)
, actionName VARCHAR2(2000)
, actionNr INTEGER
, actionResult CHAR(1)
, actionLogChannelId VARCHAR2(36)
, actionLoggingText CLOB
, actionErrors INTEGER
, actionLogDate DATE
, actionDuration INTEGER
, actionExitStatus INTEGER
, actionNrFilesRetrieved INTEGER
, actionFilename VARCHAR2(255)
, actionComment VARCHAR2(255)
, actionReason VARCHAR2(255)
)
;