# 파인 튜닝 상태 확인
fine_tune_status = client.fine_tunes.retrieve(id='ftjob-syzZZ4SyhxEmES28JKMO2PDi')

print(fine_tune_status)
