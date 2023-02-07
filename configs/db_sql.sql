

CREATE TABLE IF NOT EXISTS Logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modul VARCHAR(255) NOT NULL,
    text VARCHAR(255) NOT NULL,
    lvl  VARCHAR(255) NOT NULL, 
    info VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) 
CREATE TABLE IF NOT EXISTS hoster (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    priority INT(9), 
    regex1 VARCHAR(255),
    regex2 VARCHAR(255),
    regex3 VARCHAR(255),
    status varchar(25) NOT NULL CHECK (status IN ('working','test','new','ERROR')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_changed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) 



ALTER TABLE `EpisodeRequests` CHANGE `Title` `Title` LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL; 
ALTER TABLE `MovieRequests` CHANGE `Title` `Title` LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL; 
#test it only with this option + a movie with äüö Or only cast in view 
ALTER TABLE `TvRequests` CHANGE `Title` `Title` LONGTEXT CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL; 
#V3
 CREATE OR REPLACE VIEW WorkToDo AS SELECT
    `Ombi`.`EpisodeRequests`.`Id` AS `EpiReqId`,
    FALSE AS `isMovie`,
    `Ombi`.`EpisodeRequests`.`SeasonId` AS `SeasonId`,
    `Ombi`.`SeasonRequests`.`ChildRequestId` AS `RequestId`,
    `Ombi`.`TvRequests`.`Title` AS `Serie`,
    `Ombi`.`SeasonRequests`.`SeasonNumber` AS `SeasonNr`,
    `Ombi`.`EpisodeRequests`.`EpisodeNumber` AS `EpisodeNumber`,
    `Ombi`.`TvRequests`.`TvDbId` AS `TvDbId`,
    `Ombi`.`TvRequests`.`ImdbId` AS `ImdbId`,
    `Ombi`.`TvRequests`.`Status` AS `Status`,
    `Ombi`.`EpisodeRequests`.`Title` AS `EpiTitle`,
    `Ombi`.`ChildRequests`.`Title` AS `Title`,
     CONCAT('/data/tv/',`TvRequests`.`Title`,'/Season ',`SeasonRequests`.`SeasonNumber`,'/') AS `FolderPath`,
     CONCAT(`TvRequests`.`Title`,'.S',`SeasonRequests`.`SeasonNumber`,'.E',`EpisodeRequests`.`EpisodeNumber`,'.deu.',
    `EpisodeRequests`.`Title`,'.mp4') AS `FileName`,
    `Ombi`.`ChildRequests`.`Available` AS `Available`,
    `Ombi`.`ChildRequests`.`MarkedAsAvailable` AS `MarkedAsAvailable`,
    `Ombi`.`ChildRequests`.`Denied` AS `Denied`,
    `Ombi`.`ChildRequests`.`DeniedReason` AS `DeniedReason`,
    `Ombi`.`EpisodeRequests`.`Link_Quali` AS `4K`,
    `Ombi`.`EpisodeRequests`.`Dow_Status` AS `Dow_Status`,
    `Ombi`.`EpisodeRequests`.`Check_Quali` AS `Check_Quali`,
    `Ombi`.`EpisodeRequests`.`Bs_Link` AS `Bs_Link`,
    `Ombi`.`EpisodeRequests`.`Link` AS `Link`,
    `Ombi`.`EpisodeRequests`.`Link_Quali` AS `Link_Quali`,
    `Ombi`.`EpisodeRequests`.`Alt_Link` AS `Alt_Link`,
    `Ombi`.`EpisodeRequests`.`Alt_Link_Quali` AS `Alt_Link_Quali`,
    `Ombi`.`EpisodeRequests`.`Error` AS `Error`,
    `Ombi`.`EpisodeRequests`.`Info` AS `Info`
FROM
    (
        (
            (
                `Ombi`.`EpisodeRequests`
            JOIN `Ombi`.`SeasonRequests` ON
                (
                    `Ombi`.`EpisodeRequests`.`SeasonId` = `Ombi`.`SeasonRequests`.`Id`
                )
            )
        JOIN `Ombi`.`ChildRequests` ON
            (
                `Ombi`.`SeasonRequests`.`ChildRequestId` = `Ombi`.`ChildRequests`.`Id`
            )
        )
    JOIN `Ombi`.`TvRequests` ON
        (
            `Ombi`.`ChildRequests`.`ParentRequestId` = `Ombi`.`TvRequests`.`Id`
        )
    )
UNION
SELECT
    MovieRequests.ID,
    TRUE,
    NULL,
    NULL,
    MovieRequests.Title,
    NULL,
    NULL,
    MovieRequests.TheMovieDbId,
    MovieRequests.ImdbId,
    MovieRequests.Status,
    NULL,
    MovieRequests.Title,
     CONCAT('/movies/',MovieRequests.Title,''),
     CONCAT(MovieRequests.Title,'.mp4'),
    MovieRequests.Title,
    MovieRequests.Available,
    MovieRequests.MarkedAsAvailable,
    MovieRequests.Denied,
    MovieRequests.DeniedReason,
    MovieRequests.Has4KRequest,
    MovieRequests.Dow_Status,
    MovieRequests.Check_Quali,
    MovieRequests.Bs_Link,
    MovieRequests.Link,
    MovieRequests.Link_Quali,
    MovieRequests.Alt_Link,
    MovieRequests.Alt_Link_Quali,
    MovieRequests.Error,
    MovieRequests.Info
FROM
    MovieRequests
    WHERE MovieRequests.Denied != 1 ;
 CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

    ALTER TABLE  `Ombi`.`MovieRequests`
    ALTER TABLE  `Ombi`.`EpisodeRequests`
    ADD COLUMN Dow_Status VARCHAR(255),
   ADD COLUMN Check_Quali VARCHAR(255),
   ADD COLUMN Bs_Link VARCHAR(255),
   ADD COLUMN Link VARCHAR(255),
   ADD COLUMN Link_Quali VARCHAR(255),
   ADD COLUMN Alt_Link VARCHAR(255),
   ADD COLUMN Alt_Link_Quali VARCHAR(255),
   ADD COLUMN Error VARCHAR(30),
   ADD COLUMN Info VARCHAR(255);

    ALTER TABLE  `Ombi`.`TvRequests`
   ADD COLUMN Watcher VARCHAR(255);

   #add logger for tv request with logger 

ALTER TABLE`Ombi`.`TvRequests` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE`Ombi`.`MovieRequests` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE`Ombi`.`SeasonRequests` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE`Ombi`.`EpisodeRequests` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE`Ombi`.`ChildRequests` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
   CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

INSERT INTO `hoster` (`id`, `name`, `priority`, `regex1`, `regex2`, `regex3`, `status`, `created_at`, `last_changed`) VALUES
(1, 'Vidoza', 1, NULL, NULL, NULL, 'working', '2022-12-13 22:47:38', '2022-12-13 22:47:38'),
(3, 'Streamtape', 2, NULL, NULL, NULL, 'working', '2022-12-13 22:47:56', '2022-12-13 22:47:56'),
(4, 'StreamZ', 3, NULL, NULL, NULL, 'working', '2022-12-13 22:48:15', '2022-12-13 22:48:15'),
(6, 'StreamZZ', 4, NULL, NULL, NULL, 'working', '2022-12-13 22:48:15', '2022-12-13 22:48:15');

v4

CREATE OR REPLACE VIEW WorkToDo AS 
SELECT
    EpisodeRequests.Id AS EpiReqId,
    FALSE AS isMovie,
    EpisodeRequests.SeasonId AS SeasonId,
    SeasonRequests.ChildRequestId AS RequestId,
    TvRequests.Title AS Serie,
    LPAD(SeasonRequests.SeasonNumber, 2, '0') AS SeasonNr,
    LPAD(EpisodeRequests.EpisodeNumber, 2, '0') AS EpisodeNumber,
    TvRequests.TvDbId AS TvDbId,
    TvRequests.ImdbId AS ImdbId,
    TvRequests.Status AS Status,
    EpisodeRequests.Title AS EpiTitle,
    ChildRequests.Title AS Title,
    AspNetUsers.UserName AS UserName,
    CONCAT(IF( AspNetUsers.UserName != 'heinz',  '/tv/','/tv-opa/'), TvRequests.Title, '/Season ',  LPAD(SeasonRequests.SeasonNumber, 2, '0'), '/') AS FolderPath,
    CONCAT(TvRequests.Title, '.S', LPAD(SeasonRequests.SeasonNumber, 2, '0'), '.E', LPAD(EpisodeRequests.EpisodeNumber, 2, '0'), '.deu.', EpisodeRequests.Title, '.mp4') AS File_Name,
    ChildRequests.Available AS Available,
    ChildRequests.MarkedAsAvailable AS MarkedAsAvailable,
    ChildRequests.Denied AS Denied,
    ChildRequests.DeniedReason AS DeniedReason,
    EpisodeRequests.Link_Quali AS '4K',
    EpisodeRequests.Dow_Status AS Dow_Status,
    EpisodeRequests.Check_Quali AS Check_Quali,
    EpisodeRequests.Bs_Link AS Bs_Link,
    EpisodeRequests.Link AS Link,
    EpisodeRequests.Link_Quali AS Link_Quali,
    EpisodeRequests.Alt_Link AS Alt_Link,
    EpisodeRequests.Alt_Link_Quali AS Alt_Link_Quali,
    EpisodeRequests.Error AS Error,
    EpisodeRequests.Info AS Info
FROM
    EpisodeRequests
    JOIN SeasonRequests ON EpisodeRequests.SeasonId = SeasonRequests.Id
    JOIN ChildRequests ON SeasonRequests.ChildRequestId = ChildRequests.Id
    JOIN TvRequests ON ChildRequests.ParentRequestId = TvRequests.Id
    Join AspNetUsers ON ChildRequests.RequestedUserId = AspNetUsers.Id
UNION
SELECT
    MovieRequests.ID,
    TRUE,
    NULL,
    NULL,
    MovieRequests.Title,
    NULL,
    NULL,
    MovieRequests.TheMovieDbId,
    MovieRequests.ImdbId,
    MovieRequests.Status,
    NULL,
    MovieRequests.Title,
    AspNetUsers.UserName,
    CONCAT(IF( AspNetUsers.UserName != 'heinz',  '/movie/','/movie-opa/'), MovieRequests.Title, '/'),
    CONCAT(MovieRequests.Title, '.mp4'),
    MovieRequests.Available,
    MovieRequests.MarkedAsAvailable,
    MovieRequests.Denied,
    MovieRequests.DeniedReason,
    MovieRequests.Has4KRequest,
    MovieRequests.Dow_Status,
    MovieRequests.Check_Quali,
    MovieRequests.Bs_Link,
    MovieRequests.Link,
    MovieRequests.Link_Quali,
    MovieRequests.Alt_Link,
    MovieRequests.Alt_Link_Quali,
    MovieRequests.Error,
    MovieRequests.Info
FROM
    MovieRequests
JOIN AspNetUsers ON MovieRequests.RequestedUserId = AspNetUsers.Id
WHERE
    MovieRequests.Denied != 1;
 CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;