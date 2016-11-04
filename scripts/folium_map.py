import folium
import pandas as pd
import unicodedata

county_data = r'../data/verified_pop.csv'
county_geo = r'../assets/us_counties_20m_topo.json'

#Read into Dataframe, cast to string for consistency
df = pd.read_csv(county_data, na_values=[' '])


def set_id(fips):
    '''Modify fips code to match GeoJSON property'''

    if fips == '0':
        return None
    else:
        return ''.join(['0500000US', fips[1:6]])

#print df 
#Apply set_id, drop NaN
df['GEO_ID'] = df['fips_code'].apply(set_id)
#df = df.dropna()
print df

#Number of employed with auto scale
map_1 = folium.Map(location=[48, -102], zoom_start=3)
map_1.choropleth(geo_path=county_geo, data_out='data1.json', data=df,
        columns=['fips_code','population'],
        key_on='feature.id',
        fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.3,
        topojson='objects.us_counties_20m')
map_1.save('map_1.html')
