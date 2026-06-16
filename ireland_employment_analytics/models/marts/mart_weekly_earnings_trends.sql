with weekly as (

    select * from {{ ref('stg_weekly_earnings') }}

),

final as (

    select
        year,
        quarter,
        quarter_num,
        economic_sector,
        unit,

        avg(case when statistic_label = 'Average Weekly Earnings'
            then value end)                     as avg_weekly_earnings,

        avg(case when statistic_label = 'Average Hourly Earnings'
            then value end)                     as avg_hourly_earnings,

        avg(case when statistic_label = 'Average Weekly Hours Worked'
            then value end)                     as avg_weekly_hours,

        -- year on year growth calculation
        avg(case when statistic_label = 'Average Weekly Earnings'
            then value end)
        - lag(avg(case when statistic_label = 'Average Weekly Earnings'
            then value end))
        over (partition by economic_sector order by year, quarter_num)
                                                as weekly_earnings_yoy_change

    from weekly
    group by
        year,
        quarter,
        quarter_num,
        economic_sector,
        unit

)

select * from final