export CUDA_VISIBLE_DEVICES=6
cd /apdcephfs_cq10/share_2992827/shennong_6_public/cyuzhou/VEGA

python3.9 /apdcephfs_cq10/share_2992827/shennong_6_public/cyuzhou/VEGA/ITA.py \
    --model_path /apdcephfs_cq10/share_2992827/shennong_6_public/cyuzhou/model/qwen_0_0_200 \
    --output_path /apdcephfs_cq10/share_2992827/shennong_6_public/cyuzhou/VEGA/test.json \
    --test_file_path /apdcephfs_cq10/share_2992827/shennong_6_public/cyuzhou/VEGA/ITA_3picture_test.json