drop function if exists get_map_attribute_data;
create or replace function get_map_attribute_data(p_resourceinstanceid uuid, nodeid uuid) returns jsonb as
    $$
declare
    l_heritage_site_geom_node_id text = '1b6235b0-0d0f-11ed-98c2-5254008afee6';
    l_heritage_site_legislative_act_id text = '1f28339e-3b93-11ee-b4c5-080027b7463b';

    l_leg_act_authority_node_id text = '7789d580-3b87-11ee-a701-080027b7463b';
    data jsonb;
begin
    if nodeid = l_heritage_site_geom_node_id::uuid then -- Heritage Site

    -- Legislative Act tile in Heritage Site
        with heritage_site as (select r.resourceinstanceid,
                                      (r.descriptors->'en'->>'name') displayname,
                                      (r.descriptors->'en'->>'map_popup') map_popup,
                                      (tiledata -> l_heritage_site_legislative_act_id -> 0 ->> 'resourceId')::uuid legislative_act_id/*, * */
                               from resource_instances r join tiles t on r.resourceinstanceid = t.resourceinstanceid
                               where nodegroupid = '6cc30064-0d06-11ed-8804-5254008afee6'::uuid
                               and r.resourceinstanceid = p_resourceinstanceid /*(select nodegroupid
                                                    from nodes n
                                                    where n.nodeid = l_heritage_site_legislative_act_id::uuid)*/),
             authorities as (select resourceinstanceid,
                                    __arches_get_concept_label((tiledata ->> l_leg_act_authority_node_id)::uuid) authority/*, */
                             from tiles
                             where nodegroupid = '7789d580-3b87-11ee-a701-080027b7463b'::uuid /*((select nodegroupid
                                                   from nodes n
                                                   where n.nodeid = l_leg_act_authority_node_id::uuid))*/)
        select jsonb_build_object('displayname',displayname, 'map_popup', map_popup, 'authorities', array_agg(distinct authority))
        into data
        from heritage_site hs
                 left join authorities a on a.resourceinstanceid = hs.legislative_act_id
        where hs.resourceinstanceid = p_resourceinstanceid
        group by hs.resourceinstanceid, displayname, map_popup;
    end if;
    return data;
end;
$$
    language plpgsql;