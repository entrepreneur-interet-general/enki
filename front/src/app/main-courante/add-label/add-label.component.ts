import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { MessagesService, Tag } from '../messages.service';

@Component({
  selector: 'app-add-label',
  templateUrl: './add-label.component.html',
  styleUrls: ['./add-label.component.scss']
})
export class AddLabelComponent implements OnInit {
  labelSearch = new FormControl('')
  selectedLabels: Array<Tag>

  constructor(
    public messagesService: MessagesService
  ) {
    this.selectedLabels = []
    messagesService.getLabels().subscribe(labels => {
      this.messagesService.tags = labels
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

  sort(labels): Array<Tag> {
    return labels.sort(this.compare)
  }

  addLabel(): void {
    this.messagesService.addTag(this.labelSearch.value).subscribe(label => {
      this.messagesService.tags = this.messagesService.tags.concat(label)
      this.selectLabel(label)
      this.labelSearch.setValue('')
    })
  }

  unselectLabel(labelToUnselect): void {
    this.selectedLabels = this.selectedLabels.filter(label => label.uuid !== labelToUnselect.uuid)
  }

  selectLabel(label): void {
    this.selectedLabels = this.selectedLabels.concat(label)
  }

  getLabels(): void {

  }
}
