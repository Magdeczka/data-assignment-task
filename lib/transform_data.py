import ast
import os
import pandas as pd
from os.path import isfile, join


class Tranformator:
    """
    Class reading data from the files, transforming and saving into
    """
    DATA_PATH = "data"
    ARTICLE_READ_EVENTS = ["article_viewed"]
    ARTICLE_VIEWED_EVENTS = ["top_news_card_viewed", "my_news_card_viewed"]
    COLUMN_NAMES = ['TIMESTAMP', 'MD5(USER_ID)', 'EVENT_NAME', 'MD5(SESSION_ID)', 'article_id']

    def tranform_all_folder_files(self, folder):
        """
        :param folder: folder where all data files are placed
        :return: final_df - data frame of all articles in the data folder
        """
        file_names = [f for f in os.listdir(folder) if isfile(join(folder, f))]
        final_df = pd.DataFrame(columns = self.COLUMN_NAMES)
        for file in file_names:
            file_path = os.path.join(self.DATA_PATH, file)
            final_df = final_df.append(self.get_data(file_path))
        return final_df


    def extract_id_from_attributes(self, attributes, value):
        """
        :param value: value of attribute to be extracted
        :return:
        """
        extract_value = value
        attributes_dict = ast.literal_eval(attributes)
        # In some rows id is written with capital letters in most it's small,
        # so making sure both cases are considered
        if extract_value == "id":
            extract_value = "id" if "id" in attributes_dict else "ID"
        extracted = attributes_dict[extract_value]
        return extracted


    def get_data(self, data_path):
        data_df = pd.read_csv(data_path, sep='\t')
        data_df = data_df.reset_index()

        # Filter relevant events
        all_relevant_articles = self.ARTICLE_READ_EVENTS + self.ARTICLE_VIEWED_EVENTS
        data_df = data_df.loc[data_df['EVENT_NAME'].isin(all_relevant_articles)]
        data_df['article_id'] = data_df['ATTRIBUTES'].apply(self.extract_id_from_attributes, args=('id',))
        data_df = data_df[self.COLUMN_NAMES]
        return data_df


tr = Tranformator()
tr.tranform_all_folder_files(tr.DATA_PATH)