with
    charges as (
        select * from {{ref('stg_charges')}}
    )

select * from charges