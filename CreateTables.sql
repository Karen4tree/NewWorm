create table Users(
	user_ID varchar(255) primary key,
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
	question_ID char(8) primary key,
	asker_ID varchar(255),
	detail text,
	title varchar(255),
	answers_num int,
	followers_num int,
	foreign key (asker_ID) references Users(user_ID)
);

create table Topic(
	topic_id char(8) primary key,
	topic_name varchar(255),
	question_num int,
	followers_num int
);

create table Answers(
	answer_ID char(8) primary key,
	question_ID char(8),
	author_ID varchar(255),
	detail text,
	upvote int,
	visit_times int,
	foreign key (question_ID) references Questions(question_ID),
	foreign key (author_ID) references Users(user_ID)
);

create table Comment(
	author_ID varchar(255),
	answer_ID char(8),
	primary key (author_ID, answer_ID),
	foreign key (author_ID) references Users(user_ID),
	foreign key (answer_ID) references Answers(answer_ID)
);

create table Collection(
	collection_id char(8) primary key,
	name varchar(255),
	creator varchar(255),
	foreign key (creator) references Users(user_ID)
);

create table Follow_Question(
	question_ID char(8),
	follower_ID varchar(255),
	foreign key (question_ID) references Questions(question_ID),
	foreign key (follower_ID) references Users(user_ID),
	primary key (question_ID, follower_ID)
);

create table Follow_User(
	follower_ID varchar(255),
	followee_ID varchar(255),
	foreign key (follower_ID) references Users(user_ID),
	foreign key (followee_ID) references Users(user_ID),
	primary key (followee_ID, follower_ID)
);

create table Follow_Topic(
	follower_id varchar(255),
	topic_id char(8),
	foreign key (follower_id) references Users(user_ID),
	foreign key (topic_id) references Topic(topic_id),
	primary key (follower_id, topic_id)
);

create table Question_Topics(
	question_ID char(8),
	topic_id char(8),
	foreign key (question_ID) references Questions(question_ID),
	foreign key (topic_id) references Topic(topic_id),
	primary key (question_ID, topic_id)
);

create table Vote_Answer(
	voter_id varchar(255),
	answer_id char(8),
	foreign key (voter_id) references Users(user_ID),
	foreign key (answer_id) references Answers(answer_id),
	primary key (voter_id, answer_id)
);

create table Collection_Answers(
	collection_id char(8),
	answer_ID char(8),
	foreign key (collection_id) references Collection(collection_id),
	foreign key (answer_ID) references Answers(answer_ID),
	primary key (collection_id, answer_ID)
);

create table Articles(
	article_id char(8) primary key,
	owner_id varchar(255),
	comment_num int,
	foreign key (owner_id) references Users(user_ID)
);
