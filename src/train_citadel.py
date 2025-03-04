from transformers import AutoConfig

from args import Args
from modeling_module.citadel import CITADEL
from data_module.ir_data_module import IRTripletDataModule
from training_and_evaluating_module.ir_trainer import CITADELIRTripletTrainer

args = Args()
args.name_or_path = 'vinai/phobert-base-v2'
args.model_max_length = 256
args.no_sep = True
# args.processed_data_dir = '../data/zalo_qa/ms_marco_format/preprocessed'
args.queries_path = '../data/zalo_qa/ms_marco_format/queries_ws.tsv'
args.collection_path = '../data/zalo_qa/ms_marco_format/collection_ws.tsv'
args.train_triples_path = '../data/zalo_qa/ms_marco_format/train_triples.tsv'
args.val_qrels_path = '../data/zalo_qa/ms_marco_format/dev_qrels.tsv'
args.tok_embedding_dim = 32
args.cls_embedding_dim = 128
args.coil_score_type = 'full'
args.dataloader_num_workers = 0
args.batch_size = 8
args.padding = False
args.truncation = True
args.citadel_score_type = 'full'
args.expert_regularization_coef = 0
args.expert_load_balancing_coef = 0
args.seed = 42
args.num_train_epochs = 5
args.max_train_steps = 1_000_000
args.output_dir = '/kaggle/working/output'
args.checkpointing_steps = 6000
args.mixed_precision = 'fp16'
args.use_8bit_optimizer = False
args.lr_warmup_steps = 6000
args.scheduler = 'linear'
args.gradient_accumulation_steps = 4
args.split_batches = False
args.lr = 3e-6
args.resume_from_checkpoint = None
args.resume_path = None
args.log_with = 'wandb'
args.exp_name = 'qazalo_ir_citadel'

model_config = AutoConfig.from_pretrained(
    pretrained_model_name_or_path=args.name_or_path,
    output_hidden_states=True
)
model = CITADEL(args=args, config=model_config)
data_module = IRTripletDataModule(
    args=args,
    tokenizer=model.tokenizer
)
trainer = CITADELIRTripletTrainer(args=args)

trainer.fit(model=model, data=data_module)