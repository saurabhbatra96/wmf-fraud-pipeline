select distinct ctrb.id, ctc.display_name, ctrb.financial_type_id, ctrb.payment_instrument_id, ctrb.receive_date,
ctrb.total_amount as "usd_amount", wce.original_currency as "currency", wce.original_amount as "total_amount",
pi.gateway, pi.payment_method, pi.country,
inet_ntoa(pf.user_ip) as user_ip, pf.server, dct.utm_medium,
substring(dct.utm_campaign,1,3) as "utm_campaign",
max(if(pfb.filter_name='getAVSResult', pfb.risk_score, NULL)) as "avs_filter",
max(if(pfb.filter_name='getCVVResult', pfb.risk_score, NULL)) as "cvv_filter",
max(if(pfb.filter_name='getScoreCountryMap', pfb.risk_score, NULL)) as "country_filter",
max(if(pfb.filter_name='getScoreEmailDomainMap', pfb.risk_score, NULL)) as "email_domain_filter",
max(if(pfb.filter_name='getScoreUtmCampaignMap', pfb.risk_score, NULL)) as "utm_filter",
max(if(pfb.filter_name='IPVelocityFilter', pfb.risk_score, NULL)) as "ip_filter",
max(if(pfb.filter_name='minfraud_filter', pfb.risk_score, NULL)) as "minfraud_filter",
'0' as "label"
from civicrm.civicrm_contribution ctrb
join drupal.contribution_tracking dct on dct.contribution_id = ctrb.id
join civicrm.civicrm_contact ctc on ctrb.contact_id = ctc.id
join civicrm.wmf_contribution_extra wce on wce.entity_id = ctrb.id
join fredge.payments_initial pi on pi.contribution_tracking_id = wce.id
join fredge.payments_fraud pf on pf.contribution_tracking_id = pi.contribution_tracking_id
join fredge.payments_fraud_breakdown pfb on pfb.payments_fraud_id = pf.id
where ctrb.contribution_status_id=1 and is_test=0 and ctrb.receive_date>='2015-03-10' and ctrb.id in (select distinct id from (select distinct id from civicrm.civicrm_contribution where contribution_status_id=1 and is_test=0 order by rand() limit 100000) t)
group by pfb.payments_fraud_id
limit $num;