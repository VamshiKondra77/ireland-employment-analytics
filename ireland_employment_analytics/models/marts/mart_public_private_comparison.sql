with public_private as (

    select * from {{ ref('stg_public_private') }}

),

final as (

    select
        year,
        quarter,
        quarter_num,
        sector_type,
        unit,

        avg(case when statistic_label = 'Average Weekly Earnings'
            then value end)                     as avg_weekly_earnings,

        avg(case when statistic_label = 'Average Hourly Earnings'
            then value end)                     as avg_hourly_earnings,

        avg(case when statistic_label = 'Average Weekly Hours Worked'
            then value end)                     as avg_weekly_hours,

        sum(case when statistic_label = 'Employment'
            then value end)                     as total_employment

    from public_private
    group by
        year,
        quarter,
        quarter_num,
        sector_type,
        unit

)

select * from final