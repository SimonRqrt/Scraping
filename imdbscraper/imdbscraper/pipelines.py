# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3
from itemadapter import ItemAdapter


class ImdbscraperPipeline:

    def open_spider(self, spider):
        self.conn = sqlite3.connect('imdb_data.db')
        self.cursor = self.conn.cursor()
        if spider.name == 'spidermovies':
            self.create_table_movies()
        elif spider.name == 'spiderseries':
            self.create_table_series()

    def create_table_movies(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS movies (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            country TEXT,
                            creators TEXT,
                            duration INTEGER,
                            episodes INTEGER,
                            genre TEXT,
                            language TEXT,
                            original_title TEXT,
                            popularity REAL,
                            rating REAL,
                            seasons INTEGER,
                            stars TEXT,
                            synopsis TEXT,
                            title TEXT,
                            year INT
                        )''')
        self.conn.commit()

    def create_table_series(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS series (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            country TEXT,
                            creators TEXT,
                            duration INTEGER,
                            episodes INTEGER,
                            genre TEXT,
                            language TEXT,
                            original_title TEXT,
                            popularity REAL,
                            rating REAL,
                            seasons INTEGER,
                            stars TEXT,
                            synopsis TEXT,
                            title TEXT,
                            year_start INT,
                            year_end INT
                        )''')
        self.conn.commit()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        spider_name = spider.name

        adapter['popularity'] = self.convert_popularity(adapter['popularity'])
        adapter['rating'] = self.convert_rating(adapter['rating'])
        adapter['year'] = self.convert_year(adapter['year'])
        adapter['original_title'] = self.clean_original_title(adapter['original_title'], adapter['title'])
        adapter['genre'] = self.clean_genre(adapter['genre'])
        # item['genre'] = ','.join(item['genre'])
        # adapter['stars'] = self.clean_stars(adapter['stars'])

        if spider_name == 'spidermovies':
            adapter['duration'] = self.convert_duration_to_minutes_movies(adapter['duration'])
            self.cursor.execute('''INSERT INTO movies (
                            country,
                            creators,
                            duration,
                            episodes,
                            genre,
                            language,
                            original_title,
                            popularity,
                            rating,
                            seasons,
                            stars,
                            synopsis,
                            title,
                            year
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (
                            adapter.get('country'),
                            adapter.get('creators'),
                            adapter.get('duration'),
                            adapter.get('episodes'),
                            adapter.get('genre'),
                            adapter.get('language'),
                            adapter.get('original_title'),
                            adapter.get('popularity'),
                            adapter.get('rating'),
                            adapter.get('seasons'),
                            adapter.get('stars'),
                            adapter.get('synopsis'),
                            adapter.get('title'),
                            adapter.get('year')
                        ))
            
        elif spider_name == 'spiderseries':
            adapter['duration'] = self.convert_duration_to_minutes_series(adapter['duration'])
            adapter['year'] = self.clean_year(adapter['year'])
            adapter['seasons'] = self.clean_seasons(adapter['seasons'])
            adapter['episodes'] = self.convert_episodes(adapter['episodes'])
            self.cursor.execute('''INSERT INTO series (
                            country,
                            creators,
                            duration,
                            episodes,
                            genre,
                            language,
                            original_title,
                            popularity,
                            rating,
                            seasons,
                            stars,
                            synopsis,
                            title,
                            year_start,
                            year_end
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (
                            adapter.get('country'),
                            adapter.get('creators'),
                            adapter.get('duration'),
                            adapter.get('episodes'),
                            adapter.get('genre'),
                            adapter.get('language'),
                            adapter.get('original_title'),
                            adapter.get('popularity'),
                            adapter.get('rating'),
                            adapter.get('seasons'),
                            adapter.get('stars'),
                            adapter.get('synopsis'),
                            adapter.get('title'),
                            adapter.get('year_start'),
                            adapter.get('year_end')
                        ))

        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()


    @staticmethod
    def convert_duration_to_minutes_movies(duration):
        if 'h' in duration:
            hours, minutes = duration.split('h')
            if 'm' in minutes:
                total_minutes = int(hours) * 60 + int(minutes[:-1])
            else:
                total_minutes = int(hours) * 60
        else:
            total_minutes = int(duration.split('m')[0])
        return total_minutes

    @staticmethod
    def convert_duration_to_minutes_series(duration):
        duration_no_blank = [s.strip() for s in duration if s.strip()]
        hours = 0
        minutes = 0
        for i in range(len(duration_no_blank)):
            n = duration_no_blank[i].strip()
            if n.isdigit():
                if i < len(duration_no_blank)-1 and duration_no_blank[i+1].strip() == 'hour':
                    hours = int(n)
                elif i > 0 and duration_no_blank[i-1].strip() == 'hour':
                    continue
                else:
                    minutes = int(n)
            elif n == 'hour':
                continue
            elif n == 'minutes':
                continue
            else:
                pass
        total_minutes = hours * 60 + minutes
        return total_minutes
    
    @staticmethod
    def convert_popularity(popularity):
        if popularity is None:
            return None
        try:
            num_popularity = ''.join(filter(str.isdigit, popularity))
            num_popularity = float(num_popularity)
        except Exception as e:
            print(f"Erreur lors du nettoyage de popularity : {e}")
            num_popularity = None
        return num_popularity
    
    @staticmethod
    def convert_rating(rating):
        try:
            num_rating = float(rating)
        except Exception as e:
            print(f"Erreur lors du nettoyage de rating : {e}")
            num_rating = None
        return num_rating
    
    @staticmethod
    def convert_year(year):
        try:
            num_year = int(year)
        except Exception as e:
            print(f"Erreur lors du nettoyage de year : {e}")
            num_year = None
        return num_year
    
    @staticmethod
    def convert_episodes(episodes):
        try:
            num_episodes = int(episodes)
        except Exception as e:
            print(f"Erreur lors du nettoyage de episodes : {e}")
            num_episodes = None
        return num_episodes
    
    @staticmethod
    def clean_original_title(original_title,title):
        if original_title is not None:
            return original_title.replace("Original title: ", "")
        else :
            return title
    
    @staticmethod
    def clean_genre(genre):
        cleaned_genre = [g for g in genre if g != "Back to top"]
        if isinstance(cleaned_genre, list):
            return ','.join(cleaned_genre)
        return cleaned_genre
    
    """@staticmethod
    def clean_stars(stars):
        cleaned_stars = []
        for star in stars:
            cleaned_stars.append(star.strip())
        return cleaned_stars"""
        
    @staticmethod
    def clean_year(year):
        years = year.split('–')
        year_start = int(years[0])
        year_end = None
        if len(years) > 1:
            year_end = int(years[1])
        return year_start, year_end
    
    @staticmethod
    def clean_seasons(seasons):
        cleaned_text = ''.join(filter(str.isdigit, seasons))
        seasons = int(cleaned_text)
        return seasons