import flet as ft
import requests
import datetime  

URL = 'https://api.open-meteo.com/v1/forecast'

GENERAL_PARAMS = {
    'latitude': 59.937500,
    'longitude': 30.308611,
    'timezone': "auto", 
}

MAIN_TEMP_PARAMS = [
    'temperature_2m', 
    'apparent_temperature',
    'wind_direction_10m',
    'wind_speed_10m',
    'weather_code',
    'relative_humidity_2m',
    'visibility',
    'surface_pressure',
]

WEEK_TEMP_PARAMS = [
    'sunrise', 
    'sunset',
    'weather_code',
    'temperature_2m_max',
    'temperature_2m_min'
]

CITY_NAME = "Saint-Petersburg, Russia"

DAYS = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun"
]

ASSET_COLOR_MAP = {
    'Clear': 'yellow',
    'Cloudy': 'white',
    'Overcast' : 'white',
    'Fog': 'white',
    'Drizzle' : 'blue',
    'Rain' : 'blue',
    'Rime ice' : 'blue',
    'Snow' : 'white',
    'Thunderstorm' : 'grey'
}

ASSET_IMAGE_MAP = {
    'Clear': './assets/forecast/clear.png',
    'Cloudy': './assets/forecast/clouds.png',
    'Overcast' : './assets/forecast/atmosphere.png',
    'Fog': './assets/forecast/atmosphere.png',
    'Drizzle' : './assets/forecast/drizzle.png',
    'Rain' : './assets/forecast/rain.png',
    'Rime ice' : './assets/forecast/snow.png',
    'Snow' : './assets/forecast/snow.png',
    'Thunderstorm' : './assets/forecast/thunderstorm.png'
}

WMO_SHORT = {
    0: 'Clear',
    1: 'Clear',
    2: 'Cloudy',
    3: 'Overcast',
    45: 'Fog',
    48: 'Rime ice',
    51: 'Drizzle',
    53: 'Drizzle',
    55: 'Drizzle',
    56: 'Drizzle',
    57: 'Drizzle',
    61: 'Rain',
    63: 'Rain',
    65: 'Rain',
    66: 'Rain',
    67: 'Rain',
    71: 'Snow',
    73: 'Snow',
    75: 'Snow',
    77: 'Snow',
    80: 'Rain',
    81: 'Rain',
    82: 'Rain',
    85: 'Snow',
    86: 'Snow',
    95: 'Thunderstorm',
    96: 'Thunderstorm',
    99: 'Thunderstorm'
}


WMO_LONG = {
    0: 'Clear sky',
    1: 'Mainly clear',
    2: 'Partly cloudy',
    3: 'Overcast',
    45: 'Fog',
    48: 'Rime ice',
    51: 'Light drizzle',
    53: 'Moderate drizzle',
    55: 'Dense drizzle',
    56: 'Light freezing drizzle',
    57: 'Dense freezing drizzle',
    61: 'Slight rain',
    63: 'Moderate rain',
    65: 'Heavy rain',
    66: 'Freezing light rain',
    67: 'Freezing heavy rain',
    71: 'Slight snow fall',
    73: 'Moderate snow fall',
    75: 'Heavy snow fall',
    77: 'Snow grains',
    80: 'Slight rain shower',
    81: 'Moderate rain shower',
    82: 'Violent rain shower',
    85: 'Slight snow showers',
    86: 'Heavy snow showers',
    95: 'Thunderstorm',
    96: 'Thunderstorm with slight hail',
    99: 'Thunderstorm with heavy hail'
}

_current = requests.get(URL, params=GENERAL_PARAMS | {'current': MAIN_TEMP_PARAMS} | {'daily': WEEK_TEMP_PARAMS})


def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    
    def _expand(e):
        if e.data == "true":
            _c.content.controls[1].height = 560
            _c.content.controls[1].update()
        else:
            _c.content.controls[1].height = 660 * 0.40
            _c.content.controls[1].update()
    
    
    def _current_temp():
        _current_json = _current.json()
        _current_temp = round(_current_json['current']['temperature_2m'])
        
        _current_wmo = _current_json['current']['weather_code']
        _current_weather = WMO_SHORT.get(_current_wmo, "Unknown")
        _current_description = WMO_LONG.get(_current_wmo, "Unknown")
        _current_wind = round(_current_json['current']['wind_speed_10m'])
        _current_humidity = _current_json['current']['relative_humidity_2m']
        _current_feels = round(_current_json['current']['apparent_temperature'])
        
        return [
            _current_temp,
            _current_weather,
            _current_description,
            _current_wind,
            _current_humidity,
            _current_feels,    
        ]
      
        
    def _current_extra():
        _extra_info = []
        
        _extra = [
            [
                int(_current.json()['current']['visibility'] / 1000),
                'km',
                'Visibility',
                './assets/visibility.png',
            ],
            [
                round(_current.json()['current']['surface_pressure'] / 1.33, 2),
                'mmHg',
                'Pressure',
                './assets/pressure.png',
            ],
            [
                datetime.datetime.fromisoformat(
                    _current.json()['daily']['sunrise'][0]
                ).strftime('%H:%M'),
                '',
                'Sunrise',
                './assets/sunrise.png',
            ],
            [
                datetime.datetime.fromisoformat(
                    _current.json()['daily']['sunset'][0]
                ).strftime('%H:%M'),
                '',
                'Sunset',
                './assets/sunset.png',
            ],
        ]
        
        for data in _extra:
            _extra_info.append(
                ft.Container(
                    bgcolor='white10',
                    border_radius=12,
                    alignment=ft.alignment.center,
                    content=ft.Column(
                        alignment='center',
                        horizontal_alignment='center',
                        spacing=25,
                        controls=[
                            ft.Container(
                                alignment=ft.alignment.center,
                                content=ft.Image(
                                    src=data[3],
                                    color='white',
                                ),
                                width=32,
                                height=32,
                            ),
                            ft.Container(
                                content=ft.Column(
                                    alignment='center',
                                    horizontal_alignment='center',
                                    spacing=0,
                                    controls=[
                                        ft.Text(
                                            f'{data[0]} {data[1]}',
                                            size=14,
                                        ),
                                        ft.Text(
                                            f'{data[2]}',
                                            size=11,
                                            color='white54'
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                )
            )
        
        return _extra_info
    
    
    def _top() -> ft.Container:
        _today = _current_temp()
        
        _today_extra = ft.GridView(
            max_extent=150,
            expand=1,
            run_spacing=5,
            spacing=5,
        )
        
        for info in _current_extra():
            _today_extra.controls.append(info)
                
        top = ft.Container(
            width=310,
            height=660 * 0.4,
            gradient=ft.LinearGradient(
                begin=ft.alignment.bottom_left,
                end=ft.alignment.top_right,
                colors=["lightblue600", "lightblue900"],
            ),
            border_radius=35,
            animate=ft.animation.Animation(
                duration=350,
                curve="decelerate",
            ),
            on_hover=lambda e: _expand(e),
            padding=15,
            content=ft.Column(
                alignment='start',
                spacing=10,
                controls=[
                    ft.Row(
                        alignment='center',
                        controls=[
                            ft.Text(
                                CITY_NAME,
                                size=16,
                                weight='w500'
                            )
                        ]
                    ),
                    ft.Container(padding=ft.padding.only(bottom=5)),
                    ft.Row(
                        alignment='center',
                        spacing=30,
                        controls=[
                            ft.Column(
                               controls=[
                                   ft.Container(
                                       width=90,
                                       height=90,
                                       image_src='./assets/cloudy.png',
                                   ),
                               ],
                            ),
                            ft.Column(
                                spacing=5,
                                horizontal_alignment='center',
                                controls=[
                                    ft.Text(
                                        "Today",
                                        size=12,
                                        text_align='center'
                                    ),
                                    
                                    ft.Row(
                                        vertical_alignment='start',
                                        spacing=0,
                                        controls=[
                                            ft.Container( # Temperature
                                                content=ft.Text(
                                                    _today[0],
                                                    size=52,
                                                ),
                                            ),
                                            
                                            ft.Container( # Celcius
                                                content=ft.Text(
                                                    "°",
                                                    size=28,
                                                    text_align='center'
                                                ),
                                            ),
                                        ],
                                    ),
                                    ft.Text(
                                        _today[1],
                                        size=10,
                                        color='white54',
                                        text_align='center'
                                    ),
                                ],
                            ),
                        ],
                    ),
                    ft.Divider(height=8, thickness=1, color='white10'),
                    ft.Row(
                        alignment='spaceAround',
                        controls=[
                            ft.Container(
                                content=ft.Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        ft.Container( # Wind
                                            alignment=ft.alignment.center,
                                            content=ft.Image(
                                                src='./assets/wind.png',
                                                color='white'
                                            ),
                                            width=20,
                                            height=20,
                                        ),
                                        ft.Text( 
                                            f'{_today[3]} km/h',
                                            size=11,
                                        ),
                                        ft.Text( 
                                            'Wind',
                                            size=9,
                                            color='white54',
                                        ),
                                    ],
                                ),
                            ),
                            ft.Container(
                                content=ft.Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        ft.Container( # Humidity
                                            alignment=ft.alignment.center,
                                            content=ft.Image(
                                                src='./assets/humidity.png',
                                                color='white'
                                            ),
                                            width=20,
                                            height=20,
                                        ),
                                        ft.Text( 
                                            f'{_today[4]}%',
                                            size=11,
                                        ),
                                        ft.Text( 
                                            'Humidity',
                                            size=9,
                                            color='white54',
                                        ),
                                    ],
                                ),
                            ),
                            ft.Container(
                                content=ft.Column(
                                    horizontal_alignment='center',
                                    spacing=2,
                                    controls=[
                                        ft.Container( # Feels
                                            alignment=ft.alignment.center,
                                            content=ft.Image(
                                                src='./assets/celsius.png',
                                                color='white'
                                            ),
                                            width=20,
                                            height=20,
                                        ),
                                        ft.Text( 
                                            f'{_today[5]}°',
                                            size=11,
                                        ),
                                        ft.Text( 
                                            'Feels like',
                                            size=9,
                                            color='white54',
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                    _today_extra,
                ],
            ),
        )
        
        return top
    
    def _bottom_data():
        _bottom_data = []
        
        for index in range(7):
            _bottom_data.append(
                ft.Row(
                    spacing=5,
                    alignment='spaceBetween',
                    controls=[
                        ft.Row(
                            expand=1,
                            alignment='start',
                            controls=[
                                ft.Container(
                                    alignment=ft.alignment.center,
                                    content=ft.Text(
                                        DAYS[
                                            datetime.datetime.weekday(datetime.datetime.fromisoformat(_current.json()['daily']['sunset'][index]))
                                        ],
                                    ),
                                ),
                            ],
                        ),
                        ft.Row(
                            expand=1,
                            controls=[
                                ft.Container(
                                   content=ft.Row(
                                       alignment='start',
                                       controls=[
                                           ft.Container(
                                               width=20,
                                               height=20,
                                               alignment=ft.alignment.center_left,
                                               content=ft.Image(
                                                   src=ASSET_IMAGE_MAP[WMO_SHORT[_current.json()['daily']['weather_code'][index]]],
                                                   color=ASSET_COLOR_MAP[WMO_SHORT[_current.json()['daily']['weather_code'][index]]],
                                               ),
                                           ),
                                           ft.Text(
                                               WMO_SHORT[_current.json()['daily']['weather_code'][index]],
                                               size=11,
                                               color='white54',
                                               text_align='center',
                                           ),
                                       ],
                                   ), 
                                ),
                            ],
                        ),
                        ft.Row(
                            expand=1,
                            alignment='end',
                            controls=[
                                ft.Container(
                                    alignment=ft.alignment.center,
                                    content=ft.Row(
                                        alignment='center',
                                        spacing=5,
                                        controls=[
                                            ft.Container(
                                                width=20,
                                                content=ft.Text(
                                                    str(int(_current.json()['daily']['temperature_2m_max'][index])) + '°',
                                                    text_align='start',
                                                ),
                                            ),
                                            ft.Container(
                                                width=20,
                                                content=ft.Text(
                                                    str(int(_current.json()['daily']['temperature_2m_min'][index])) + '°',
                                                    text_align='end',
                                                ),
                                            ),
                                        ],
                                    ),
                                ),
                            ],
                        )
                    ],
                )
            )
            
        return _bottom_data
    
    def _bottom() -> ft.Container:
        _bot_column = ft.Column(
            alignment='center',
            horizontal_alignment='center',
            spacing=25,
        )
        
        for data in _bottom_data():
            _bot_column.controls.append(data)
        
        bottom = ft.Container(
            padding=ft.padding.only(
                top=280, 
                left=20, 
                right=20, 
                bottom=20
            ),
            content=_bot_column
        )
        
        return bottom
    
    
    _c = ft.Container(
        width=310,
        height=660,
        border_radius=35,
        bgcolor='black',
        padding=10,
        content=ft.Stack(
            width=300, 
            height=550, 
            controls=[
                _bottom(),
                _top(),
            ],
        ),
    )
    
    page.add(_c)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")