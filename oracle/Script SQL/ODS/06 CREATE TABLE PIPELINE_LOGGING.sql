CREATE TABLE ODS.PIPELINE_LOGGING
(
  loggingDate DATE
, loggingPhase VARCHAR2(2000)
, pipelineName VARCHAR2(255)
, pipelineFilename VARCHAR2(255)
, pipelineStart DATE
, pipelineEnd DATE
, pipelineLogChannelId VARCHAR2(36)
, parentLogChannelId VARCHAR2(36)
, pipelineLogging CLOB
, pipelineErrorCount INTEGER
, pipelineStatusDescription VARCHAR2(32)
, transformName VARCHAR2(2000)
, transformCopyNr INTEGER
, transformStatusDescription VARCHAR2(100)
, transformLogChannelId VARCHAR2(36)
, transformLoggingText CLOB
, transformLinesRead INTEGER
, transformLinesWritten INTEGER
, transformLinesInput INTEGER
, transformLinesOutput INTEGER
, transformLinesUpdated INTEGER
, transformLinesRejected INTEGER
, transformErrors INTEGER
, transformStart DATE
, transformEnd DATE
, transformDuration INTEGER
)
;