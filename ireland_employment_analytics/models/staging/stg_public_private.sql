with source as (

    select * from {{ source('raw', 'raw_public_private') }}

),

renamed as (

    select
        statistic_label,
        quarter,
        sector_type,
        unit,
        value,
        left(quarter, 4)::integer   as year,
        right(quarter, 2)           as quarter_num

    from source
    where value is not null

)

select * from renamed