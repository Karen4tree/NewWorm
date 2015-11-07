create table Users(
	user_id varchar(255) primary key,
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
	education varchar(255),
	education_extra varchar(255),
	location varchar(255),
	business varchar(255),
	position varchar(255),
	employment varchar(255)
);

create table Questions(
	question_id char(8) primary key,
	asker_id varchar(255),
	detail text,
	title varchar(255),
	answers_num int,
	followers_num int,
	foreign key (asker_id) references Users(user_id)
);

create table Topic(
	topic_id char(8) primary key,
	topic_name varchar(255),
	question_num int,
	followers_num int
);

create table Answers(
	answer_id char(8) primary key,
	question_id char(8),
	author_id varchar(255),
	detail text,
	upvote int,
	visit_times int,
	foreign key (question_id) references Questions(question_id),
	foreign key (author_id) references Users(user_id)
);

create table Comment(
	author_id varchar(255),
	answer_id char(8),
	primary key (author_id, answer_id),
	foreign key (author_id) references Users(user_id),
	foreign key (answer_id) references Answers(answer_id)
);

create table Collection(
	collection_id char(8) primary key,
	name varchar(255),
	creator varchar(255),
	foreign key (creator) references Users(user_id)
);

create table Follow_Question(
	question_id char(8),
	follower_id varchar(255),
	foreign key (question_id) references Questions(question_id),
	foreign key (follower_id) references Users(user_id),
	primary key (question_id, follower_id)
);

create table Follow_User(
	follower_id varchar(255),
	followee_id varchar(255),
	foreign key (follower_id) references Users(user_id),
	foreign key (followee_id) references Users(user_id),
	primary key (followee_id, follower_id)
);

create table Follow_Topic(
	follower_id varchar(255),
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

create table Vote_Answer(
	voter_id varchar(255),
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
	column_name varchar(255) primary key,
	owner_id varchar(255),
	follower_num int,
	foreign key (owner_id) references Users(user_id)
);

create table Articles(
	article_id char(8) primary key,
	column_name varchar(255),
	article_title varchar(255),
	comment_num int,
	detail text,
	foreign key (column_name) references Columns(column_name)
);

create table Follow_Column(
	follower_id varchar(255),
	column_name varchar(255),
	foreign key (follower_id) references Users(user_id),
	foreign key (column_name) references Columns(column_name),
	primary key (follower_id, column_name)
);
