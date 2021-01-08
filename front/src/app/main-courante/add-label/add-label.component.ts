import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MessagesService } from '../messages.service';
import { Label, LabelsService } from '../labels.service';


@Component({
  selector: 'app-add-label',
  templateUrl: './add-label.component.html',
  styleUrls: ['./add-label.component.scss']
})
export class AddLabelComponent implements OnInit {
  labelSearch = new FormControl('')

  constructor(
    public messagesService: MessagesService,
    public labelsService: LabelsService
  ) {
    labelsService.getLabels().subscribe(labels => {
      this.labelsService.labels = labels
    })
  }

  ngOnInit(): void {
  }

  compare(a, b): any {
    if (a.title.toLowerCase() < b.title.toLowerCase()) {
      return -1;
    }
    if (a.title.toLowerCase() > b.title.toLowerCase()) {
      return 1;
    }
    return 0;
  }

  sort(labels): Array<Label> {
    return labels.sort(this.compare)
  }

  addLabel(): void {
    this.labelsService.addLabel(this.labelSearch.value).subscribe(label => {
      this.labelsService.labels = this.labelsService.labels.concat(label)
      this.selectLabel(label)
      this.labelSearch.setValue('')
    })
  }

  unselectLabel(labelToUnselect): void {
    this.labelsService.selectedLabels = this.labelsService.selectedLabels.filter(label => label.uuid !== labelToUnselect.uuid)
  }

  selectLabel(label): void {
    this.labelsService.selectedLabels = this.labelsService.selectedLabels.concat(label)
  }

  getLabels(): void {

  }
}
