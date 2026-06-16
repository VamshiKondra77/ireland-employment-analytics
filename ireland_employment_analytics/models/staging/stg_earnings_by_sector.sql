with source as (

    select * from {{ source('raw', 'raw_earnings_by_sector') }}

),

renamed as (

    select
        statistic_label,
        quarter,
        economic_sector,
        type_of_employee,
        unit,
        value,
        left(quarter, 4)::integer   as year,
        right(quarter, 2)           as quarter_num

    from source
    where value is not null

)

select * from renamed