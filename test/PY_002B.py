import numpy as np
import pandas as pd
from math import pi
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

csv_url = 'https://covid19.isciii.es/resources/serie_historica_acumulados.csv'


class GetCovidDataModel(object):
    def __init__(self, path_graph=None, dpi=200):
        self.path_graph = path_graph
        self.dpi = dpi

    def get_covid_statistics(self):
        df_raw = self._clean_data_frame(self._csv_to_data_frame(csv_url))
        df_raw['Fecha'] = pd.to_datetime(df_raw['FECHA'], format='%d/%m/%Y')
        df_raw.sort_values(by='Fecha', ascending=False, inplace=True)
        df_raw['Fecha'] = df_raw['Fecha'].dt.date
        df_dates = df_raw.copy()
        df_dates.drop_duplicates(subset='Fecha', inplace=True)
        last_date = self._get_last_date(df_raw, 'Fecha', 'FECHA')

        df_raw['CASOS'] = pd.to_numeric(df_raw['CASOS'], downcast='integer')
        df_raw['Hospitalizados'] = pd.to_numeric(df_raw['Hospitalizados'], downcast='integer')
        df_raw['UCI'] = pd.to_numeric(df_raw['UCI'], downcast='integer')
        df_raw['Fallecidos'] = pd.to_numeric(df_raw['Fallecidos'], downcast='integer')
        df_raw['Recuperados'] = pd.to_numeric(df_raw['Recuperados'], downcast='integer')
        df_aggregated = pd.DataFrame(columns=['Date', 'Infected', 'InHospital', 'UCI', 'Death', 'Recupered'])

        print(df_raw['CASOS'].sum())
        for i, row in df_dates.iterrows():
            df_by_date = df_raw[df_raw['Fecha'] == row['Fecha']]
            line = {'Date': row[1],
                    'Infected': df_by_date['CASOS'].sum(),
                    'InHospital': df_by_date['Hospitalizados'].sum(),
                    'UCI': df_by_date['UCI'].sum(),
                    'Death': df_by_date['Fallecidos'].sum(),
                    'Recupered': df_by_date['Recuperados'].sum()}
            df_aggregated = df_aggregated.append(line, ignore_index=True)
        df_aggregated['Date'] = pd.to_datetime(df_aggregated['Date'], format='%d/%m/%Y')
        df_aggregated['Date'] = df_aggregated['Date'].dt.date
        df_aggregated.sort_values(by='Date', ascending=True, inplace=True)
        total_infected = df_aggregated.iloc[-1, 1]
        total_inhospital = df_aggregated.iloc[-1, 2]
        total_uci = df_aggregated.iloc[-1, 3]
        total_death = df_aggregated.iloc[-1, 4]
        total_recupered = df_aggregated.iloc[-1, 5]

        s_progress_yesterday = df_aggregated.iloc[-2]
        s_progress_today = df_aggregated.iloc[-1]
        progress_absolute = {'Infected': s_progress_today['Infected'] - s_progress_yesterday['Infected'],
                             'InHospital': s_progress_today['InHospital'] - s_progress_yesterday['InHospital'],
                             'UCI': s_progress_today['UCI'] - s_progress_yesterday['UCI'],
                             'Death': s_progress_today['Death'] - s_progress_yesterday['Death'],
                             'Recupered': s_progress_today['Recupered'] - s_progress_yesterday['Recupered']
                             }

        progress_percentage = {'Infected %': round(
            (((s_progress_today['Infected'] - s_progress_yesterday['Infected']) / s_progress_today['Infected']) * 100), 2),
                               'InHospital %': round((((s_progress_today['InHospital'] - s_progress_yesterday[
                                   'InHospital']) / s_progress_today['InHospital']) * 100), 2),
                               'UCI %': round((((s_progress_today['UCI'] - s_progress_yesterday['UCI']) / s_progress_today[
                                   'UCI']) * 100), 2),
                               'Death %': round((((s_progress_today['Death'] - s_progress_yesterday['Death']) /
                                                  s_progress_today['Death']) * 100), 2),
                               'Recupered %': round((((s_progress_today['Recupered'] - s_progress_yesterday['Recupered']) /
                                                      s_progress_today['Recupered']) * 100), 2),
                               }

        df_daily_progress_abs = pd.DataFrame()
        df_daily_progress_pct = pd.DataFrame()
        df_daily_progress_abs = df_daily_progress_abs.append(progress_absolute, ignore_index=True)
        df_daily_progress_pct = df_daily_progress_pct.append(progress_percentage, ignore_index=True)

        plt.figure('COVID-19: Global situation in Spain', figsize=(24, 10))
        plt.suptitle('Last update to {date}'.format(date=last_date))

        ax1 = plt.subplot(212)
        label_infected = 'Infected: ' + str(int(total_infected))
        label_inhospital = 'In Hospital: ' + str(int(total_inhospital))
        label_uci = 'UCI: ' + str(int(total_uci))
        label_deaths = 'Deaths: ' + str(int(total_death))
        label_recupered = 'Recupered: ' + str(int(total_recupered))
        '''Plot outputs: We can plot the fit line over the data'''
        x1 = df_aggregated['Infected']
        x2 = df_aggregated['InHospital']
        x3 = df_aggregated['UCI']
        x4 = df_aggregated['Death']
        x5 = df_aggregated['Recupered']
        y = df_aggregated['Date']

        plt.title('Historical')
        line1 = ax1.plot(y, x1, linestyle='solid', label=label_infected)
        line2 = ax1.plot(y, x2, dashes=[6, 2], label=label_inhospital)
        line3 = ax1.plot(y, x3, dashes=[6, 2], label=label_uci)
        line4 = ax1.plot(y, x4, dashes=[6, 2], label=label_deaths)
        line5 = ax1.plot(y, x5, dashes=[6, 2], label=label_recupered)

        ax1.xaxis.set_major_locator(MultipleLocator(3))
        ax1.use_sticky_edges = False
        ax1.tick_params(labelrotation=45)
        ax1.legend()

        ax2 = plt.subplot(221)
        labels = ('Infected', 'In Hospital', 'UCI', 'Death', 'Recupered')
        y_pos = np.arange(len(labels))
        data = [df_daily_progress_abs.iloc[0, 2],
                df_daily_progress_abs.iloc[0, 1],
                df_daily_progress_abs.iloc[0, 4],
                df_daily_progress_abs.iloc[0, 0],
                df_daily_progress_abs.iloc[0, 3]]

        ax2.barh(y_pos, data, align='center', alpha=0.2)
        for i, value in enumerate(data):
            plt.text(value + 3, i + .25, str(int(value)), va='center')
        plt.title('Absolute Values: Lastest').set_position([.5, 1.10])
        plt.yticks(y_pos, labels)

        categories = list(df_daily_progress_pct)
        N = len(categories)

        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        ax3 = plt.subplot(222, polar=True)

        ax3.set_theta_offset(pi / 2)
        ax3.set_theta_direction(-1)
        plt.xticks(angles[:-1], categories)
        ax3.set_rlabel_position(30)
        plt.yticks(color="grey", size=7)
        plt.ylim(0, int(max(df_daily_progress_pct.max())) + 1)

        values = df_daily_progress_pct.loc[0].values.flatten().tolist()
        values += values[:1]
        ax3.plot(angles, values, 'r', alpha=0.5, linewidth=1, linestyle='solid', )
        ax3.fill(angles, values, 'r', alpha=0.1)

        plt.title('Relative Values: Comparing against yesterday').set_position([.5, 1.10])

        if self.path_graph is None:
            mng = plt.get_current_fig_manager()
            mng.resize(*mng.window.maxsize())
            plt.show()
            return

        plt.savefig(self.path_graph)
        return self.path_graph

    @staticmethod
    def _csv_to_data_frame(csv):
        data_frame = pd.read_csv(
            csv,
            # names=['CCAA', 'FECHA', 'CASOS', 'Hospitalizados', 'UCI', 'Fallecidos', 'Recuperados'],
            usecols=['CCAA', 'FECHA', 'CASOS', 'Hospitalizados', 'UCI', 'Fallecidos', 'Recuperados'],
            encoding='ISO-8859-1',
            delimiter=','
            # skiprows=1
        )
        return data_frame

    @staticmethod
    def _clean_data_frame(data_frame):
        data_frame_clean = data_frame[data_frame.CCAA.map(len) < 3]
        df_clean = data_frame_clean.copy()
        return df_clean

    @staticmethod
    def _get_last_date(data_frame, sort_key, filter_key):
        return data_frame.sort_values(by=sort_key)[filter_key].iloc[-1]


covid = GetCovidDataModel(path_graph='image.png', dpi=200)
covid.get_covid_statistics()
