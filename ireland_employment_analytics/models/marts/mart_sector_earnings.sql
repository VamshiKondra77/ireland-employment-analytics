with earnings as (

    select * from {{ ref('stg_earnings_by_sector') }}

),

final as (

    select
        year,
        quarter,
        quarter_num,
        economic_sector,
        type_of_employee,
        unit,

        sum(case when statistic_label = 'Employment'
            then value end)                         as total_employment,

        avg(case when statistic_label = 'Average Weekly Earnings'
            then value end)                         as avg_weekly_earnings,

        avg(case when statistic_label = 'Average Hourly Earnings'
            then value end)                         as avg_hourly_earnings,

        avg(case when statistic_label = 'Average Weekly Hours Worked'
            then value end)                         as avg_weekly_hours

    from earnings
    group by
        year,
        quarter,
        quarter_num,
        economic_sector,
        type_of_employee,
        unit

)

select * from final