CREATE TABLE `atlas_claims` (
	`id` varchar(80) NOT NULL,
	`status` varchar(24) NOT NULL,
	`tone` varchar(24) NOT NULL,
	`domain` varchar(120) NOT NULL,
	`title` text NOT NULL,
	`summary` text NOT NULL,
	`source` text NOT NULL,
	`limitation` text NOT NULL,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `atlas_claims_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `atlas_datasets` (
	`id` int AUTO_INCREMENT NOT NULL,
	`name` varchar(160) NOT NULL,
	`scope` text NOT NULL,
	`artifact` text NOT NULL,
	`provenance` text NOT NULL,
	`color` varchar(16) NOT NULL,
	CONSTRAINT `atlas_datasets_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `atlas_publications` (
	`id` int AUTO_INCREMENT NOT NULL,
	`type` varchar(80) NOT NULL,
	`year` varchar(12) NOT NULL,
	`title` text NOT NULL,
	`summary` text NOT NULL,
	`href` text NOT NULL,
	`tag` varchar(80) NOT NULL,
	CONSTRAINT `atlas_publications_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `atlas_release_state` (
	`id` int AUTO_INCREMENT NOT NULL,
	`version` varchar(80) NOT NULL,
	`researchRelease` varchar(160) NOT NULL,
	`commit` varchar(80) NOT NULL,
	`note` text NOT NULL,
	`linksJson` text NOT NULL,
	`isCurrent` int NOT NULL DEFAULT 1,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `atlas_release_state_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `atlas_timeline` (
	`id` int AUTO_INCREMENT NOT NULL,
	`date` varchar(40) NOT NULL,
	`title` text NOT NULL,
	`body` text NOT NULL,
	CONSTRAINT `atlas_timeline_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `atlas_workstreams` (
	`id` varchar(80) NOT NULL,
	`label` varchar(160) NOT NULL,
	`short` text NOT NULL,
	`status` varchar(24) NOT NULL,
	`progress` int NOT NULL,
	`color` varchar(16) NOT NULL,
	CONSTRAINT `atlas_workstreams_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `research_files` (
	`id` int AUTO_INCREMENT NOT NULL,
	`title` varchar(240) NOT NULL,
	`category` varchar(80) NOT NULL,
	`description` text,
	`fileName` varchar(240) NOT NULL,
	`mimeType` varchar(160) NOT NULL,
	`sizeBytes` int NOT NULL,
	`storageKey` text NOT NULL,
	`publicUrl` text NOT NULL,
	`checksum` varchar(128),
	`visibility` enum('public','private') NOT NULL DEFAULT 'public',
	`uploadedBy` int,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `research_files_id` PRIMARY KEY(`id`),
	CONSTRAINT `research_files_storageKey_unique` UNIQUE(`storageKey`)
);
--> statement-breakpoint
CREATE TABLE `theory_bridges` (
	`id` varchar(80) NOT NULL,
	`label` varchar(160) NOT NULL,
	`description` text NOT NULL,
	`fromNode` varchar(80) NOT NULL,
	`toNode` varchar(80) NOT NULL,
	CONSTRAINT `theory_bridges_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `theory_nodes` (
	`id` varchar(80) NOT NULL,
	`number` varchar(8) NOT NULL,
	`title` varchar(120) NOT NULL,
	`detail` text NOT NULL,
	`status` varchar(24) NOT NULL,
	CONSTRAINT `theory_nodes_id` PRIMARY KEY(`id`)
);
--> statement-breakpoint
CREATE TABLE `users` (
	`id` int AUTO_INCREMENT NOT NULL,
	`openId` varchar(64) NOT NULL,
	`name` text,
	`email` varchar(320),
	`loginMethod` varchar(64),
	`role` enum('user','admin') NOT NULL DEFAULT 'user',
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	`lastSignedIn` timestamp NOT NULL DEFAULT (now()),
	CONSTRAINT `users_id` PRIMARY KEY(`id`),
	CONSTRAINT `users_openId_unique` UNIQUE(`openId`)
);
