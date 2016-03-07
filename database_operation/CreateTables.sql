SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ALLOW_INVALID_DATES';
ALTER DATABASE zhihu CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
create table Users(
	user_id varchar(191) primary key,
	followers_num int,
	followees_num int,
	agrees_num int,
	thanks_num int,
	asks_num int,
	answers_num int,
	articles_num int,
	collections_num int,
	following_topics_num int,
	following_columns int,
	education varchar(191),
	education_extra varchar(191),
	location varchar(191),
	business varchar(191),
	position varchar(191),
	employment varchar(191)
);

create table Questions(
	question_id char(8) primary key,
	asker_id varchar(191),
	detail text,
	title varchar(191),
	answers_num int,
	followers_num int,
	post_time TIMESTAMP,
	last_update_time TIMESTAMP,
	opinion int,
	foreign key (asker_id) references Users(user_id)
);

create table Topic(
	topic_id char(8) primary key,
	topic_name varchar(191),
	question_num int,
	followers_num int,
	visited int
);

create table Answers(
	answer_id char(8),
	question_id char(8),
	author_id varchar(191),
	detail text,
	upvote int,
	visit_times int,
	post_time TIMESTAMP,
	last_edit_time TIMESTAMP,
	opinion int,
	foreign key (question_id) references Questions(question_id),
	foreign key (author_id) references Users(user_id),
	PRIMARY KEY (answer_id,question_id)
);

create table Comment(
	author_id varchar(191),
	answer_id char(8),
	opinion int,
	primary key (author_id, answer_id),
	foreign key (author_id) references Users(user_id),
	foreign key (answer_id) references Answers(answer_id)
);

create table Collection(
	collection_id char(8) primary key,
	name varchar(191),
	creator varchar(191),
	foreign key (creator) references Users(user_id)
);

create table Follow_Question(
	question_id char(8),
	follower_id varchar(191),
	foreign key (question_id) references Questions(question_id),
	foreign key (follower_id) references Users(user_id),
	primary key (question_id, follower_id)
);

create table Follow_User(
	follower_id varchar(191),
	followee_id varchar(191),
	foreign key (follower_id) references Users(user_id),
	foreign key (followee_id) references Users(user_id),
	primary key (followee_id, follower_id)
);

create table Follow_Topic(
	follower_id varchar(191),
	topic_id char(8),
	foreign key (follower_id) references Users(user_id),
	foreign key (topic_id) references Topic(topic_id),
	primary key (follower_id, topic_id)
);

create table Question_Topics(
	question_id char(8),
	topic_id char(8),
	foreign key (question_id) references Questions(question_id),
	foreign key (topic_id) references Topic(topic_id),
	primary key (question_id, topic_id)
);

create table Topic_Topics(
	father_topid_id char(8),
	child_topid_id char(8),
	foreign key (father_topid_id) references Topic(topic_id),
	foreign key (child_topid_id) references Topic(topic_id),
	primary key (father_topid_id, child_topid_id)
);

create table Vote_Answer(
	voter_id varchar(191),
	answer_id char(8),
	foreign key (voter_id) references Users(user_id),
	foreign key (answer_id) references Answers(answer_id),
	primary key (voter_id, answer_id)
);

create table Collection_Answers(
	collection_id char(8),
	answer_id char(8),
	foreign key (collection_id) references Collection(collection_id),
	foreign key (answer_id) references Answers(answer_id),
	primary key (collection_id, answer_id)
);

create table Columns(
	column_name varchar(191) primary key,
	owner_id varchar(191),
	follower_num int,
	foreign key (owner_id) references Users(user_id)
);

create table Articles(
	article_id char(8) primary key,
	column_name varchar(191),
	article_title varchar(191),
	comment_num int,
	detail text,
	foreign key (column_name) references Columns(column_name)
);

create table Follow_Column(
	follower_id varchar(191),
	column_name varchar(191),
	foreign key (follower_id) references Users(user_id),
	foreign key (column_name) references Columns(column_name),
	primary key (follower_id, column_name)
);
